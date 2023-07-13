import json, yaml
from langchain.chat_models import ChatOpenAI
from src.tools.neo4j.base import Neo4jManager
from src.tools.extractor.base import init_extract_chain
from src.procedure.extract_and_insert.base import extract_entities_from_paper

with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

llm = ChatOpenAI(temperature=0.3)
extract_chain = init_extract_chain(llm)

db_manager = Neo4jManager()