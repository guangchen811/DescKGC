import argparse

from langchain.chat_models import ChatOpenAI

from AutoKGC.procedures.align_across_subgraphs.base import (
    get_entity_type_uuids,
    query_from_specific_type_uuids,
    select_candidate_entities_uuids,
    align_source_and_candidates_with_chain,
)
from AutoKGC.procedures.load_config import load_config
from AutoKGC.tools.align.base import init_align_chain
from AutoKGC.tools.align.parser import AlignOutputParser
from AutoKGC.tools.db_manager.base import DBManager


def main(entity_types):
    db_manager = DBManager(**config["neo4jdb"], **config["chromadb"])
    llm = ChatOpenAI(temperature=config["llm"]["temperature"])
    topic = config["topic"]
    align_chain = init_align_chain(llm=llm)
    align_parser = AlignOutputParser()
    entity_type_uuids_dict = get_entity_type_uuids(db_manager, entity_types)

    for entity_type, uuids in entity_type_uuids_dict.items():
        for uuid in uuids:
            similar_entities = query_from_specific_type_uuids(db_manager, [entity_type], uuid)
            candidate_uuids = select_candidate_entities_uuids(
                threshold=config["entity_alignment"]["threshold"],
                similar_entities=similar_entities,
                src_entity_uuid=uuid,
            )
            if len(candidate_uuids) > 0:
                entities = align_source_and_candidates_with_chain(
                    topic, db_manager, align_chain, align_parser, uuid, candidate_uuids
                )
                for entity in entities:
                    print(entity)
                    # TODO: complete the following function
                    # db_manager.create_alignment_relationship(
                    #     uuid, entity[0], entity[1]
                    # )
                break
        break


if __name__ == "__main__":
    config = load_config()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--entity_types",
        type=list,
        default=config["entity_alignment"]["entity_types"],
    )
    args = parser.parse_args()
    main(entity_types=args.entity_types)
