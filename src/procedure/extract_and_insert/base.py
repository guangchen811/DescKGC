from .utils import (
    entity_relation_format,
    add_one_entity,
    add_one_relation
)

def extract_entities_from_paper(paper_id_type, paper_id_value, topic, shortenings, db_manager, extract_chain):
    entity_list, relation_triple_list = entity_relation_format(paper_id_type, paper_id_value, topic, db_manager, extract_chain)
    entity_id_dict = {}
    for entity in entity_list:
        entity_shortning = shortenings[entity['type']]
        elementid = add_one_entity(db_manager, paper_id_type, paper_id_value, entity, entity_shortning)
        entity_id_dict[entity['name']] = elementid
    for relation_triple in relation_triple_list:
        add_one_relation(db_manager, relation_triple, entity_id_dict)

def extract_entities_from_papers(id_type, id_value_list, topic, shortenings, db_manager, extract_chain):
    for id_value in id_value_list:
        extract_entities_from_paper(id_type, id_value, topic, shortenings, db_manager, extract_chain)

def get_paper_title_by_filed(db_manager, field_name):
    # return paper titles who have field_name
    query = "MATCH (p:Paper) WHERE p.{} IS NOT NULL RETURN p.title AS titles".format(field_name)
    res = db_manager.graph.query(query)
    return [r['titles'] for r in res]