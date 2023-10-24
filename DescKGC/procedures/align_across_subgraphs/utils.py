import time
import uuid


def add_one_merged_entity(db_manager, id_type, id_values, entity, shortning):
    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    uuid_ = f"{shortning}-{uuid.uuid4()}"
    _ = db_manager.graph_db.query(
        f"""
            MATCH (e) WHERE e.{id_type} IN $id_values
            WITH e
            MERGE (c:{entity['type']} {{name:$name, description:$description,
            general:$general, uuid:$uuid}})
            MERGE (c)-[r:MERGED_FROM {{timestep:$timestep}}]->(e)
            RETURN elementid(c) AS elementid
            """,
        params={
            "id_values": id_values,
            "name": entity["name"],
            "description": entity["description"],
            "general": entity["general"],
            "timestep": time_str,
            "uuid": uuid_,
        },
    )
    return uuid_
