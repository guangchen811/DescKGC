from pydantic import BaseModel


class Neo4jDBSettings(BaseModel):
    url: str = "bolt://localhost:7687"
    username: str = "neo4j"
    password: str = "123.x.abc"


class ChromaDBSettings(BaseModel):
    chroma_db_impl: str = "duckdb+parquet"
    persist_directory: str = "./data/chroma/"
    collection_name: str = "default_collection"
    distance_function: str = "l2"


class ArxivExtractorSettings(BaseModel):
    data_path: str = "./data/arxiv/"
    vs_key_info: dict = {"embedding_key": "summary", "metadata_keys": ["title"]}


class EntityExtractorSettings(BaseModel):
    vs_key_info: dict = {"embedding_key": "description", "metadata_keys": ["name", "general", "type"]}


class LLMSettings(BaseModel):
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.3


class ShorteningsSettings(BaseModel):
    Paper: str = "p"
    Concept: str = "c"
    Model: str = "m"
    Dataset: str = "d"


class EntityAlignmentSettings(BaseModel):
    entity_types: list = ["Concept", "Model", "Dataset"]
    threshold: float = 0.08


class AutoKGCConfig(BaseModel):
    topic: str = "network science"
    neo4jdb: Neo4jDBSettings = Neo4jDBSettings()
    chromadb: ChromaDBSettings = ChromaDBSettings()
    extractor: dict = {"arxiv": ArxivExtractorSettings(), "entity": EntityExtractorSettings()}
    llm: LLMSettings = LLMSettings()
    shortenings: ShorteningsSettings = ShorteningsSettings()
    entity_alignment: EntityAlignmentSettings = EntityAlignmentSettings()
