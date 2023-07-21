import yaml
import argparse
from src.tools.db_manager.base import DBManager
from src.procedure.align_across_subgraphs.base import (
    get_entity_type_uuids,
    query_from_specific_type_uuids,
    select_candidate_entities_uuids
)
from src.tools.align.base import init_align_chain
with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser()
parser.add_argument('--entity_types', type=list, default=config['entity_alignment']['entity_types'])
args = parser.parse_args()

db_manager = DBManager(**config['neo4jdb'], **config['chromadb'])
entity_type_uuids_dict = get_entity_type_uuids(db_manager, args.entity_types)
for entity_type, uuids in entity_type_uuids_dict.items():
    for uuid in uuids:
        similar_entities = query_from_specific_type_uuids(db_manager, [entity_type], uuid)
        candidate_uuids = select_candidate_entities_uuids(threshold=config['entity_alignment']['threshold'], similar_entities=similar_entities, src_entity_uuid=uuid)
        if len(candidate_uuids) > 0:
            print(f"Source entity: {uuid}")
            print(f"Target entities: {candidate_uuids}")
    break