SystemInstructionTemplate = """For this task, you are given a text description and a list of entities mentioned in the text. Your goal is to identify relationships between these entities based on the description.

Here's how to do it:

1. Read the text and the list of entities carefully.
2. Look for direct relationships between pairs of entities in the list. A relationship is considered 'direct' if it's explicitly mentioned in the text.
3. Represent each identified relationship as a triple: (entity1, relation, entity2), where 'entity1' and 'entity2' are entities from the list and 'relation' represents the relationship between them.
"""
HumanExampleTemplate = """The description reads:
```
{example_description}
```
the required relations are:
```
{example_required_relations}
```
Please write down the triples.
"""
AIExampleTemplate = """The triples are:
```
{example_triples}
```
"""
HumanInputTemplate = """The description reads:
```
{description}
```
the required relations are:
```
{required_relations}
```
Please write down the triples.
"""