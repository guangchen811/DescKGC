import json, yaml
import argparse
from langchain.chat_models import ChatOpenAI
from src.tools.neo4j.base import Neo4jManager
from src.tools.extractor.base import init_extract_chain
from src.procedure.extract_and_insert.base import extract_entities_from_paper, get_paper_title_by_filed
with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser()
parser.add_argument('--id_type', type=str)
parser.add_argument('--id_value', type=str)
parser.add_argument('--temperature', type=float, default=config['llm']['temperature'])
args = parser.parse_args()

llm = ChatOpenAI(temperature=args.temperature)
extract_chain = init_extract_chain(llm)
db_manager = Neo4jManager()

# print(db_manager.graph_schema)
# title = 'The Sharing Economy for the Smart Grid'
# extract_entities_from_paper(id_type='title', id_value=title, db_manager=db_manager, extract_chain=extract_chain)
res = get_paper_title_by_filed(db_manager, 'doi')
for title in res:
    extract_entities_from_paper(id_type='title', id_value=title, db_manager=db_manager, extract_chain=extract_chain)