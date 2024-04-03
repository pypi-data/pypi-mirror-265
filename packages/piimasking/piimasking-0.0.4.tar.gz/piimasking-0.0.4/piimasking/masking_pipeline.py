import spacy
from gliner_spacy.pipeline import GlinerSpacy
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from collections import defaultdict
from datetime import datetime
from azure.data.tables import TableServiceClient


class LoadedSpacyNlpEngine(SpacyNlpEngine):
    def __init__(self, loaded_spacy_model):
        super().__init__()
        self.nlp = {"en": loaded_spacy_model}


class MaskingPipeline:

    def __init__(self, connection_string) -> None:
        self.labels = ["PERSON", "PHONE_NUMBER", "EMAIL_ADDRESS", "ORG"]
        self.anonymizer = AnonymizerEngine()
        self.download_spacy_models()
        self.nlp_sm = spacy.load("en_core_web_sm")
        self.nlp_sm.add_pipe(
            "gliner_spacy", config={"gliner_model": "urc/gliner_base", "labels": self.labels}
        )
        self.nlp_md = spacy.load("en_core_web_md")

        self.loaded_nlp_engine = LoadedSpacyNlpEngine(loaded_spacy_model=self.nlp_sm)

        self.analyzer = AnalyzerEngine(nlp_engine=self.loaded_nlp_engine)
        self.conn_str = connection_string
        self.table_name = 'piimaskingdumps'
        self.table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
        self.table_client = self.table_service.get_table_client(table_name=self.table_name)


    def download_spacy_models(self):
        try:
            spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading language model for the spaCy POS tagger")
            from spacy.cli import download
            download("en_core_web_sm")
            print("Download complete. Loading the model...")
            spacy.load("en_core_web_sm")

        # Repeat for other models
        try:
            spacy.load("en_core_web_md")
        except OSError:
            from spacy.cli import download
            download("en_core_web_md")


    def get_organizations_from_models(self, text, models):
        all_orgs = defaultdict(bool)
        for model in models:
            doc = model(text)
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    all_orgs[ent.text] = True
        return all_orgs


    def anonymize(self, original_text: str) -> str:
        text = original_text
        analyzer_results = self.analyzer.analyze(text=text, entities=self.labels, language="en")

        replacements = []

        for result in analyzer_results:
            if result.entity_type != "PERSON":
                replacement_text = "[PHONE NUMBER]" if result.entity_type == "PHONE_NUMBER" else \
                                "[EMAIL]" if result.entity_type == "EMAIL_ADDRESS" else ""
                
                replacements.append((result.start, result.end, replacement_text))

        person_id_map = {}
        current_person_id = 1
        for result in analyzer_results:
            if result.entity_type == "PERSON":
                entity_text = text[result.start:result.end]
                if entity_text not in person_id_map:
                    person_id_map[entity_text] = f"Person {current_person_id}"
                    current_person_id += 1
                replacements.append((result.start, result.end, person_id_map[entity_text]))

        replacements.sort(key=lambda x: -x[0])

        for start, end, replacement_text in replacements:
            text = text[:start] + replacement_text + text[end:]

        orgs_from_both_models = self.get_organizations_from_models(text, [self.nlp_sm, self.nlp_md])
        
        for org in orgs_from_both_models.keys():
            text = text.replace(org, f"Organization{list(orgs_from_both_models.keys()).index(org) + 1}")
        
        self.store_texts(original_text, text)

        return text


    def store_texts(self, original_text, masked_text):
        partition_key = "TextData"
        row_key = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

        entity = {
            'PartitionKey': partition_key,
            'RowKey': row_key,
            'OriginalText': original_text,
            'MaskedText': masked_text
        }

        self.table_client.create_entity(entity=entity)
        # print(f"Stored text pair with RowKey: {row_key}")
        