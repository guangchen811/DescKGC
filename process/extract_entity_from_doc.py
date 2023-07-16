import json
import yaml
import argparse
from langchain.chat_models import ChatOpenAI
from src.tools.db_manager.base import DBManager
from src.tools.extractor.base import init_extract_chain
from src.procedure.extract_and_insert.base import extract_entities_from_paper, get_paper_title_by_field
with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser()
parser.add_argument('--id_type', type=str)
parser.add_argument('--id_value', type=str)
parser.add_argument('--temperature', type=float,
                    default=config['llm']['temperature'])
args = parser.parse_args()

llm = ChatOpenAI(temperature=args.temperature)
extract_chain = init_extract_chain(llm)
db_manager = DBManager(**config['neo4jdb'], **config['chromadb'])

res = get_paper_title_by_field(db_manager, 'doi')
for title in res:
    extract_entities_from_paper(
        paper_id_type='title',
        paper_id_value=title,
        topic=config['topic'],
        shortenings=config['shortenings'],
        vs_key_info=config['extractor']['entity']['vs_key_info'],
        db_manager=db_manager,
        extract_chain=extract_chain,
    )
