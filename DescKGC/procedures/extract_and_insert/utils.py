import json
import re
import time
import uuid


def convert_to_triples(input_string):
    # Use regular expressions to find all substrings that look like '( ... )'
    triple_strings = re.findall(r"\((.*?)\)", input_string)
    triples = []
    for string in triple_strings:
        # Split by ', ' and append as a tuple
        triple = string.split(", ")
        triples.append(tuple(triple))
    return triples


def entity_relation_format(
    id_type, id_value, topic, db_manager, extract_chain
):
    "Return a list of entities and a list of relations"
    summary = db_manager.graph_db.query(
        f"""MATCH (n:Paper) WHERE n.{id_type}=$id_value
        RETURN n.summary as summary""",
        params={"id_value": id_value},
    )
    res = extract_chain({"topic": topic, "summary": summary})
    try:
        entity_list = json.loads(res["entities"])
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to decode JSON string: {str(e)}")
        return [], []
    try:
        relation_list = convert_to_triples(res["relations"])
    except Exception as e:
        print(f"Failed to decode triples from relations: {str(e)}")
        return [], []
    return entity_list, relation_list


def add_one_entity(db_manager, id_type, id_value, entity, shortning):
    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    uuid_ = f"{shortning}-{uuid.uuid4()}"
    _ = db_manager.graph_db.query(
        f"""
            MATCH (p:Paper) WHERE p.{id_type}=$id_value
            WITH p
            MERGE (c:{entity['type']} {{name:$name, description:$description,
            general:$general, uuid:$uuid}})
            MERGE (c)-[r:EXTRACTED_FROM {{timestep:$timestep}}]->(p)
            RETURN elementid(c) AS elementid
            """,
        params={
            "id_value": id_value,
            "name": entity["name"],
            "description": entity["description"],
            "general": entity["general"],
            "timestep": time_str,
            "uuid": uuid_,
        },
    )
    return uuid_


def add_one_relation(db_manager, relation_triple, entity_uuid_dict):
    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    try:
        src_uuid, dst_uuid = (
            entity_uuid_dict[relation_triple[0]],
            entity_uuid_dict[relation_triple[2]],
        )
    except Exception as e:
        print(f"Error: Inconsistent Entity Extraction - {str(e)}")
        print(
            """Details: The entities present in the relation triples were not
            previously added as nodes during the entity extraction phase."""
        )
        print(
            """Suggestion: Ensure that the Language Model maintains consistency
            between the entity extraction and relation extraction steps."""
        )
        return
    relation_name = relation_triple[1].upper().replace(" ", "_")
    db_manager.graph_db.query(
        f"""
            MATCH (src) WHERE src.uuid=$src_uuid
            MATCH (dst) WHERE dst.uuid=$dst_uuid
            MERGE (src)-[rel: {relation_name} {{timestep: $timestep}}]->(dst)
            """,
        params={
            "src_uuid": src_uuid,
            "dst_uuid": dst_uuid,
            "timestep": time_str,
        },
    )
