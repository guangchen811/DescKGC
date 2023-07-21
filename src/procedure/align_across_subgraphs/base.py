from ...tools.db_manager.type import DBManagerType

def get_entity_type_nodes(db_manager: DBManagerType, entity_types: list) -> dict:
    assert isinstance(entity_types, list), "entity_types should be a list"
    entity_type_nodes = {node_type: [] for node_type in entity_types}
    for node_type in entity_types:
        uuids = db_manager.vector_store.get_specific_type_nodes_uuid(node_type)
        entity_type_nodes[node_type] = uuids
    return entity_type_nodes

def query_from_specific_type_nodes(db_manager: DBManagerType, target_entity_types: list, query_entity_uuid: str) -> list:
    query = db_manager.vector_store.get_by_uuid(
        uuid=[query_entity_uuid])['documents'][0]

    results = db_manager.vector_store.query_from_specific_type(target_entity_types, query, n_results=10)
    return results

def select_candidate_entities(db_manager: DBManagerType, threshold: float, similar_entities):
    raise NotImplementedError