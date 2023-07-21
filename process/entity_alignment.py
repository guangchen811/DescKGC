import yaml
import argparse
from src.tools.db_manager.base import DBManager
from src.procedure.align_across_subgraphs.base import (
    get_entity_type_nodes,
    query_from_specific_type_nodes,
    select_candidate_entities
)
with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser()
parser.add_argument('--entity_types', type=list, default=config['entity_alignment']['entity_types'])
args = parser.parse_args()

db_manager = DBManager(**config['neo4jdb'], **config['chromadb'])
entity_type_nodes_dict = get_entity_type_nodes(db_manager, args.entity_types)
for entity_type, nodes in entity_type_nodes_dict.items():
    for node in nodes:
        similar_entities = query_from_specific_type_nodes(db_manager, [entity_type], node)
        candidate_entities = select_candidate_entities
        break
    break