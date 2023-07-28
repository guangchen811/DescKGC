from typing import List, Type

from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

from AutoKGC.tools.align.utils import entities_warpper
from AutoKGC.tools.db_manager.type import DBManagerType


def get_entity_type_uuids(db_manager: DBManagerType, entity_types: list) -> dict:
    assert isinstance(entity_types, list), "entity_types should be a list"
    entity_type_uuids = {node_type: [] for node_type in entity_types}
    for node_type in entity_types:
        uuids = db_manager.vector_db.get_specific_type_nodes_uuid(node_type)
        entity_type_uuids[node_type] = uuids
    return entity_type_uuids


def query_from_specific_type_uuids(
    db_manager: DBManagerType,
    target_entity_types: list,
    query_entity_uuid: str,
) -> list:
    query = db_manager.vector_db.get_by_uuid(uuid=[query_entity_uuid])["documents"][0]

    results = db_manager.vector_db.query_from_specific_type(target_entity_types, query, n_results=10)
    return results


def select_candidate_entities_uuids(threshold: float, similar_entities: dict, src_entity_uuid: str) -> list:
    "Return a list of the uuids of similar entities within the threshold"
    "distance from the source entity."

    distances = similar_entities["distances"][0]
    entity_uuids = similar_entities["ids"][0]

    # Remove source entity from options
    if entity_uuids[0] == src_entity_uuid:
        entity_uuids.pop(0)
        distances.pop(0)

    candidate_uuids = []
    for uuid, dist in zip(entity_uuids, distances):
        if dist <= threshold:
            candidate_uuids.append(uuid)
    return candidate_uuids


def align_source_and_candidates_with_chain(
    topic: str,
    db_manager: DBManagerType,
    align_chain: Type[LLMChain],
    align_parser: Type[BaseOutputParser],
    uuid: str,
    candidate_uuids: List[str],
):
    source_entity_pair = db_manager.vector_db.get_name_description_by_uuid(uuid)
    source_entity_pair_fmt = entities_warpper(source_entity_pair, is_candiate=False)
    target_entity_pairs = db_manager.vector_db.get_name_description_by_uuid(candidate_uuids)
    target_entity_pairs_fmt = entities_warpper(target_entity_pairs, is_candiate=True)
    res = align_chain(
        {
            "topic": topic,
            "source_entity": source_entity_pair_fmt,
            "candidate_entities": target_entity_pairs_fmt,
        }
    )
    entities = align_parser.parse(res["entities"])
    return entities
