import json
from langchain.chat_models import ChatOpenAI
from src.tools.neo4j.base import Neo4jManager
from src.tools.extractor.base import init_extract_chain
from src.procedure.extract_and_insert.base import extract_entities_from_paper

llm = ChatOpenAI(temperature=0.3)
extract_chain = init_extract_chain(llm)

db_manager = Neo4jManager()
# print(db_manager.graph_schema)

# title = 'Product of two staircase rank one transformations that is not loosely Bernoulli'
# extract_entities_from_paper(id_type='title', id_value=title, db_manager=db_manager, extract_chain=extract_chain)

