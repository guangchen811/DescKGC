import argparse

from langchain.chat_models import ChatOpenAI

from AutoKGC.procedure.align_across_subgraphs.base import (
    get_entity_type_uuids, query_from_specific_type_uuids,
    select_candidate_entities_uuids)
from AutoKGC.procedure.load_config import load_config
from AutoKGC.tools.align.base import init_align_chain
from AutoKGC.tools.align.parser import AlignOutputParser
from AutoKGC.tools.align.utils import entities_warpper
from AutoKGC.tools.db_manager.base import DBManager

config = load_config()

parser = argparse.ArgumentParser()
parser.add_argument('--entity_types', type=list,
                    default=config['entity_alignment']['entity_types'])
args = parser.parse_args()

db_manager = DBManager(**config['neo4jdb'], **config['chromadb'])
llm = ChatOpenAI(temperature=config['llm']['temperature'])
align_chain = init_align_chain(llm=llm)
align_parser = AlignOutputParser()
entity_type_uuids_dict = get_entity_type_uuids(db_manager, args.entity_types)

for entity_type, uuids in entity_type_uuids_dict.items():
    for uuid in uuids:
        similar_entities = query_from_specific_type_uuids(
            db_manager, [entity_type], uuid)
        candidate_uuids = select_candidate_entities_uuids(
            threshold=config['entity_alignment']['threshold'], similar_entities=similar_entities, src_entity_uuid=uuid)
        if len(candidate_uuids) > 0:
            source_entity_pair = db_manager.vector_store.get_name_description_by_uuid(
                uuid)
            source_entity_pair_fmt = entities_warpper(
                source_entity_pair, is_candiate=False)
            target_entity_pairs = db_manager.vector_store.get_name_description_by_uuid(
                candidate_uuids)
            target_entity_pairs_fmt = entities_warpper(
                target_entity_pairs, is_candiate=True)
            res = align_chain({
                "topic": config['topic'],
                "source_entity": source_entity_pair_fmt,
                "candidate_entities": target_entity_pairs_fmt
            })
            entities = align_parser.parse(res['entities'])
            for entity in entities:
                print(entity)
                # todo: complete the following function
                # db_manager.create_alignment_relationship(uuid, entity[0], entity[1])
    break
