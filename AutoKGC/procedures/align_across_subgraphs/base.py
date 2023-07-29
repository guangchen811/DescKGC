from typing import List, Tuple, Type, Dict

from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

from AutoKGC.tools.align.utils import entities_warpper
from AutoKGC.tools.db_manager.type import DBManagerType


def get_entity_type_uuids(db_manager: DBManagerType, entity_types: list) -> Dict:
    """Return a dictionary of entity types and their uuids.

    :param db_manager: DBManager object
    :type db_manager: DBManagerType
    :param entity_types: list of entity types
    :type entity_types: list
    :return: dictionary of entity types and their uuids
    :rtype: Dict
    """
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
    """Return a list of similar entities from the target entity types.

    given a query entity uuid.
    :param db_manager: DBManager object
    :type db_manager: DBManagerType
    :param target_entity_types: list of target entity types
    :type target_entity_types: list
    :param query_entity_uuid: uuid of the query entity
    :type query_entity_uuid: str
    :return: list of similar entities
    :rtype: list
    """
    query = db_manager.vector_db.get_by_uuid(uuid=[query_entity_uuid])["documents"][0]

    results = db_manager.vector_db.query_from_specific_type(target_entity_types, query, n_results=10)
    return results


def select_candidate_entities_uuids(threshold: float, similar_entities: dict, src_entity_uuid: str) -> list:
    """Return a list of the uuids of similar entities within the threshold.

    distance from the source entity.
    :param threshold: threshold distance
    :type threshold: float
    :param similar_entities: similar entities
    :type similar_entities: dict
    :param src_entity_uuid: uuid of the source entity
    :type src_entity_uuid: str
    :return: list of uuids of similar entities within the threshold distance
    :rtype: list
    """

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
) -> List[Tuple[int, str]]:
    """use the align_chain to align the source entity and the candidate entities.

    :param topic: The topic of the conversation
    :type topic: str
    :param db_manager: The database manager
    :type db_manager: DBManagerType
    :param align_chain: The align chain
    :type align_chain: Type[LLMChain]
    :param align_parser: The align parser
    :type align_parser: Type[BaseOutputParser]
    :param uuid: The uuid of the source entity
    :type uuid: str
    :param candidate_uuids: The uuids of the candidate entities
    :type candidate_uuids: List[str]
    :return: A list of tuples, each tuple contains the order of the entity and the entity name.
        For example, [(0, "entity1"), (1, "entity2")].
    :rtype: List[Tuple[int, str]]
    """

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
