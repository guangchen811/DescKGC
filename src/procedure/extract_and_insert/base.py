from .utils import (
    entity_relation_format,
    add_one_entity,
    add_one_relation
)

def extract_entities_from_paper(doi, db_manager, extract_chain):
    entity_list, relation_list = entity_relation_format(doi, db_manager, extract_chain)
    id_dict = {}
    for entity in entity_list:
        elementid = add_one_entity(db_manager, doi, entity['type'], entity['name'], entity['description'], entity['general'])
        id_dict[entity['name']] = elementid
    for relation_triple in relation_list:
        add_one_relation(db_manager, relation_triple, id_dict)