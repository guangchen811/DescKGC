from .utils import (
    entity_relation_format,
    add_one_entity,
    add_one_relation
)


def extract_entities_from_paper(paper_id_type, paper_id_value, topic, shortenings, vs_key_info, db_manager, extract_chain):
    entity_list, relation_triple_list = entity_relation_format(
        paper_id_type, paper_id_value, topic, db_manager, extract_chain)
    entity_id_dict = {}
    embedding_key = vs_key_info["embedding_key"]
    metadata_keys = vs_key_info["metadata_keys"]
    entity_keys = entity_list[0].keys()
    assert all(key in entity_keys for key in [
               embedding_key, *metadata_keys]), "KeyError: some keys are not in the paper dict. Please check the vs_key_info in config.yaml"
    for entity in entity_list:
        entity_shortning = shortenings[entity['type']]
        entity_uuid = add_one_entity(
            db_manager, paper_id_type, paper_id_value, entity, entity_shortning)
        entity_id_dict[entity['name']] = entity_uuid
        metadata = {metadata_key: entity[metadata_key]
                    for metadata_key in metadata_keys}
        metadata['embedding_key'] = 'description'
        db_manager.vector_store.add(
            documents=[entity[embedding_key]],
            metadatas=[metadata],
            ids=[entity_uuid]
        )
    for relation_triple in relation_triple_list:
        add_one_relation(db_manager, relation_triple, entity_id_dict)


def extract_entities_from_papers(id_type, id_value_list, topic, db_manager, extract_chain, config):
    shortenings = config['shortenings']
    vs_key_info = config['extractor']['entity']['vs_key_info']
    for id_value in id_value_list:
        extract_entities_from_paper(
            id_type, id_value, topic, shortenings, vs_key_info, db_manager, extract_chain)


def get_paper_title_by_field(db_manager, field_name):
    # return paper titles who have field_name
    query = "MATCH (p:Paper) WHERE p.{} IS NOT NULL RETURN p.title AS titles".format(
        field_name)
    res = db_manager.graph.query(query)
    return [r['titles'] for r in res]
