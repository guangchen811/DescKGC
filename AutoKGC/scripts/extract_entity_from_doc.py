import argparse
import json

import yaml
from langchain.chat_models import ChatOpenAI

from AutoKGC.procedure.extract_and_insert.base import (extract_entities_from_paper,
                                                   get_paper_title_by_field)
from AutoKGC.tools.db_manager.base import DBManager
from AutoKGC.tools.extractor.base import init_extract_chain
from AutoKGC.procedure.load_config import load_config

config = load_config()

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
