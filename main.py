import json
from langchain.chat_models import ChatOpenAI
from src.tools.extractor.base import init_extract_chain
from src.tools.neo4j.base import Neo4jManager

with open('./data/complex_network.json', 'r') as f:
    res = json.load(f)

llm = ChatOpenAI(temperature=0.3)
extract_chain = init_extract_chain(llm)

db_manager = Neo4jManager()
db_manager.add_from_arxiv(res)