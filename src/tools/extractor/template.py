ENTITY_EXTRACT_TEMPLATE = """You are provided with a research paper summary. Your task is to extract key entities from the summary that are related to a given topic. These entities should belong to one of the following categories:

- Concept: A concept or idea presented in the paper, e.g., "deep learning", "convolutional neural network", "attention mechanism".
- Model: A specific model discussed in the paper, e.g., "BERT", "ResNet", "Transformer".
- Dataset: A dataset used or referenced in the paper, e.g., "MNIST", "CIFAR-10", "ImageNet".

Extract all relevant entities from the summary and return them as a list. Each entity should be represented in JSON format with these keys:

- type: The category of the entity (i.e., "Concept", "Model", "Dataset").
- name: The name of the entity.
- description: A brief description of the entity, sourced from the summary.
- general: A boolean indicating if the entity is a general concept within the given topic or unique to the specific paper. For example, "language model" is a general concept within the topic "Natural Language Processing", while "a dataset of 1000 images of cats" is specific to a particular paper.


Here's an example. Given the summary "BERT is a language model proposed by Google in 2018. It is based on the Transformer architecture." and the topic "Natural Language Processing", the output should be:

[
  {{"type": "Model", "name": "BERT", "description": "BERT is a language model proposed by Google in 2018", "general": true}},
  {{"type": "Concept", "name": "Transformer", "description": "Transformer is a neural network architecture", "general": true}},
  {{"type": "Concept", "name": "language model", "description": "A language model predicts the next word given the previous words", "general": true}},
  {{"type": "Concept", "name": "neural network", "description": "A neural network is a model that learns from data", "general": true}}
]

Note: The order of entities does not matter. Do not use external resources for descriptions; all descriptions should be derived from the given summary.

Now, proceed with the following inputs:

Topic:
{topic}

Summary:
{summary}

Output Entities:

"""

RELATION_EXTRACT_TEMPLATE = """Given a research paper summary and a list of entities within the summary, your task is to extract and identify the relations between these entities.

The relations should fall into one of these categories:

- alias: Indicates that two entities are essentially the same, e.g., "BERT" and "Bidirectional Encoder Representations from Transformers".
- is superior to: Indicates a hierarchical relationship where one concept is more abstract or general than the other. For example, "language model" is superior to "BERT".
- based on: Indicates that one entity is based on another. For example, "BERT" is based on "Transformer".

The output should consist of triples: (entity1, relation, entity2), where entity1 and entity2 come from the provided entities, and relation represents a DIRECTED relationship between the two.

For instance, if the summary reads:
"BERT, also known as Bidirectional Encoder Representations from Transformers, is a language model proposed by Google in 2018. It is based on the Transformer architecture.",
and the entities are:
[
  {{"type": "Model", "name": "BERT", "description": "BERT is a language model proposed by Google in 2018", "general": true}},
  {{"type": "Model", "name": "Transformer", "description": "Transformer is a neural network architecture proposed by Google in 2017", "general": true}},
  {{"type": "Concept", "name": "language model", "description": "A language model is a model that can predict the next word given the previous words", "general": true}},
]

then the output should be:
(BERT, alias, Bidirectional Encoder Representations from Transformers)
(BERT, based on, Transformer)
(language model, is superior to, BERT)

Note: The description of relations should come directly from the summary and be as concise as possible. Do not use external resources. The DIRECTION of the relations is critical.

Now let's get started!

The input summary is

{summary}

The input entities are

{entities}

The output relations are
"""