import json, yaml
from langchain.chat_models import ChatOpenAI
from src.tools.db_manager.base import DBManager
from src.tools.extractor.base import init_extract_chain
from src.procedure.extract_and_insert.base import extract_entities_from_paper

with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

llm = ChatOpenAI(temperature=config['llm']['temperature'])
extract_chain = init_extract_chain(llm)

db_manager = DBManager(**config['neo4jdb'], **config['chromadb'])