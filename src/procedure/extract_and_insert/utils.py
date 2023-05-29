import re
import json
import time

def convert_to_triples(input_string):
    # Use regular expressions to find all substrings that look like '( ... )'
    triple_strings = re.findall(r'\((.*?)\)', input_string)
    
    triples = []
    for string in triple_strings:
        # Split by ', ' and append as a tuple
        triple = string.split(', ')
        triples.append(tuple(triple))
    
    return triples

def entity_relation_format(doi, db_manager, extract_chain):
    summary = db_manager.graph.query(
        "MATCH (n:Paper) WHERE n.doi=$doi RETURN n.summary as summary",
        params={"doi": doi}
    )
    res = extract_chain({"topic":"network science", "summary":summary})
    try:
        entity_list = json.loads(res['entities'])
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON string: {str(e)}")
    try:
        relation_list = convert_to_triples(res['relations'])
    except Exception as e:
        print(f"Failed to decode triples from relations: {str(e)}")
    return entity_list, relation_list
def add_one_entity(db_manager, doi, type, name, description, general):
    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    response = db_manager.graph.query(
            f"""
            MATCH (p:Paper) WHERE p.doi=$doi
            WITH p
            MERGE (c:{type} {{name:$name, description:$description, general:$general}})
            MERGE (c)-[r:EXTRACTED_FROM {{timestep:$timestep}}]->(p)
            RETURN elementid(c) AS elementid
            """,
            params={"doi": doi, "name": name, "description": description, "general": general, "timestep": time_str}
        )
    return response[0]['elementid']
def add_one_relation(db_manager, relation_triple, id_dict):
    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    try:
        src_id, dst_id = id_dict[relation_triple[0]], id_dict[relation_triple[2]]
    except Exception as e:
        print(f"entities in relation triples have not been added as a node: {str(e)}")
        return
    relation_name = relation_triple[1].upper().replace(' ', '_')
    db_manager.graph.query(
            f"""
            MATCH (src) WHERE elementID(src)=$src_id
            MATCH (dst) WHERE elementID(dst)=$dst_id
            MERGE (src)-[rel: {relation_name} {{timestep: $timestep}}]->(dst)
            """,
            params={'src_id': src_id, 'dst_id': dst_id, 'timestep': time_str}
        )