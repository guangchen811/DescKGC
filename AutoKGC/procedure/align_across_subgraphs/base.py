from ...tools.db_manager.type import DBManagerType


def get_entity_type_uuids(
    db_manager: DBManagerType, entity_types: list
) -> dict:
    assert isinstance(entity_types, list), "entity_types should be a list"
    entity_type_uuids = {node_type: [] for node_type in entity_types}
    for node_type in entity_types:
        uuids = db_manager.vector_store.get_specific_type_nodes_uuid(node_type)
        entity_type_uuids[node_type] = uuids
    return entity_type_uuids


def query_from_specific_type_uuids(
    db_manager: DBManagerType,
    target_entity_types: list,
    query_entity_uuid: str,
) -> list:
    query = db_manager.vector_store.get_by_uuid(uuid=[query_entity_uuid])[
        "documents"
    ][0]

    results = db_manager.vector_store.query_from_specific_type(
        target_entity_types, query, n_results=10
    )
    return results


def select_candidate_entities_uuids(
    threshold: float, similar_entities: dict, src_entity_uuid: str
) -> list:
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
