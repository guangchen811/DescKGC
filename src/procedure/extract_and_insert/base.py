from .utils import (
    entity_relation_format,
    add_one_entity,
    add_one_relation
)

def extract_entities_from_paper(id_type, id_value, db_manager, extract_chain):
    entity_list, relation_list = entity_relation_format(id_type, id_value, db_manager, extract_chain)
    id_dict = {}
    for entity in entity_list:
        elementid = add_one_entity(db_manager, id_type, id_value, entity['type'], entity['name'], entity['description'], entity['general'])
        id_dict[entity['name']] = elementid
    for relation_triple in relation_list:
        add_one_relation(db_manager, relation_triple, id_dict)