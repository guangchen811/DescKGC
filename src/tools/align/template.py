ALIGN_TASK_FORMAT_TEMPLATE = """You are a researcher in the field of {topic}. During a knowledge graph construction process, you are asked to discriminate if the candidate entity(s) describe the same concept as the source entity so that we should merge them into one entity. Each entity contains the name and description in the format of `<name>: <description>`.
Besides each candidate entity is attached with a number to make it easy to refer to. Please read the source entity and candidate entities carefully and select the correct candidate entity(s) that describe the same concept as the source entity. 
The result should be formatted as a list of numbers and names separated by comma. For example, if you think the candidate entity 1 and 3 describe the same concept as the source entity, you should return `[1 <name of entity 1>,3 <name of entity 3>]`. If you think none of the candidate entities describe the same concept as the source entity, you should return `[]`.

For example, given the source entity:
"Complex netwrok: Networks with non-trivial topological features and patterns of connection between nodes."
and the candidate entities:
[
    "1. complex network: non-trivial topological features and patterns of connection between nodes.",
    "2. small world network: a network in which most nodes are not neighbors of one another, but most nodes can be reached from every other by a small number of hops or steps.",
    "3. network science: an academic field which studies complex networks such as telecommunication networks, computer networks, biological networks, cognitive and semantic networks, and social networks."
]
You should return `[1 complex network]` because the candidate entity 1 describes the same concept as the source entity and the candidate entity 2 and 3 do not describe the same concept as the source entity."""
ALIGN_INPUT_TEMPLATE = """the source entity:
{source_entity}
the candidate entities:
{candidate_entities}
your answer:"""
