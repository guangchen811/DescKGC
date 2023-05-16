ENTITY_EXTRACT_TEMPLATE = """In this task, you are given a text description. Your goal is to identify key entities mentioned in this text. An entity could be a place, a person, an organization, etc.

Here's how to do it:

1. Read the text carefully.
2. Identify key entities that are either the 'subject' or the 'object' in a possible relationship pair. A 'subject' is the entity from which a relationship originates and an 'object' is the entity towards which the relationship is directed.
3. Represent each entity in a JSON format with the following keys:
   - 'type': The category of the entity (e.g., "place", "organization", "person").
   - 'name': The name of the entity.s

Here's an example. Given the description "浅草神社位于日本东京都台东区浅草的浅草寺本堂东侧，供奉的是土师真中知、桧田浜成、桧前武成，三位对于浅草寺创立有密切关联的人，每年5月17日都会举行三社祭。现在被指定为重要文化财产。" The topic is "建筑", the relation list is : ['事件', '位于', '名称由来'].
The output should contain the following entities (this is just an example, the actual output can be more):

[
  {{"type": "place", "name": "浅草神社"}},
    {{"type": "activaty", "name": "三社祭"}},
    {{"type": "place", "name": "浅草"}},
    {{"type": "localation", "name": "台东区"}},
]

Note: The order of entities does not matter. Do not use external resources for descriptions; all descriptions should be derived from the given description. The entities should be as specific as possible and as much as possible.

Now, proceed with the following inputs:

Topic:
{cate}

description:
{description}

relation list:

{required_relations}

Output Entities:

"""

RELATION_EXTRACT_TEMPLATE = """For this task, you are given a text description and a list of entities mentioned in the text. Your goal is to identify relationships between these entities based on the description.

Here's how to do it:

1. Read the text and the list of entities carefully.
2. Look for direct relationships between pairs of entities in the list. A relationship is considered 'direct' if it's explicitly mentioned in the text.
3. Represent each identified relationship as a triple: (entity1, relation, entity2), where 'entity1' and 'entity2' are entities from the list and 'relation' represents the relationship between them.

For instance, if the description reads:
"浅草神社位于日本东京都台东区浅草的浅草寺本堂东侧，供奉的是土师真中知、桧田浜成、桧前武成，三位对于浅草寺创立有密切关联的人，每年5月17日都会举行三社祭。现在被指定为重要文化财产。",
and the entities are:
[
    {{"type": "place", "name": "浅草神社"}},
    {{"type": "place", "name": "浅草寺"}},
    {{"type": "activaty", "name": "三社祭"}},
    {{"type": "place", "name": "浅草"}},
    {{"type": "localation", "name": "台东区"}},
]
the required relations are:
['事件', '位于', '名称由来']

then the output triples should be:
(浅草神社,事件,三社祭)
(浅草神社,位于,浅草)
(台东区,位于,东京都)
(浅草寺,位于,浅草)
(浅草寺,名称由来,浅草)

Note: The description of relations should come directly from the description and be as concise as possible. Do not use external resources. The DIRECTION of the relations is critical.

Now let's get started!

The topic is 

{cate}

The input description is

{description}

The entities are

{entities}

The required relations are

{required_relations}

The output triple relations are
"""