ENTITY_EXTRACT_TEMPLATE = """You will be given a paper summary. Your task is to extract key entities from the summary.

The entities should be fall into one of the following categories:

- conception: a concept in the paper, e.g. "deep learning", "convolutional neural network", "attention mechanism", etc.
- model: a specific model in the paper, e.g. "BERT", "ResNet", "Transformer", etc.
- dataset: a dataset used in the paper, e.g. "MNIST", "CIFAR-10", "ImageNet", etc.

You should extract all entities from the summary, and return a list of entities. Each entity should be in json format with the following keys:

- type: the type of the entity, one of "conception", "model", "dataset"
- name: the name of the entity, e.g. "BERT", "MNIST", etc.
- description: the description of the entity, e.g. "BERT is a language model proposed by Google in 2018", "MNIST is a dataset of handwritten digits", etc.

For example, if the summary is "BERT is a language model proposed by Google in 2018. It is based on the Transformer architecture.", then the output should be:
{{"type": "model", "name": "BERT", "description": "BERT is a language model proposed by Google in 2018"}}
{{"type": "conception", "name": "Transformer", "description": "Transformer is a neural network architecture proposed by Google in 2017"}}
{{"type": "conception", "name": "language model", "description": "A language model is a model that can predict the next word given the previous words"}}
{{"type": "conception", "name": "neural network", "description": "A neural network is a model that can learn from data"}}

Note that the order of the entities does not matter. The descriptions of entities should all come from the summary, and should be as biref as possible. You are not allowed to use external resources to add new descriptions.

Now, let's get started!

The input summary is

{summary}

The output entities are
"""

RELATION_EXTRACT_TEMPLATE = """given a paper summary and entities in the summary, your task is to extract the relations between the relations in the summary.

The relations should be fall into one of the following categories:
- alias: two models are aliases of each other, e.g. "BERT is also known as Bidirectional Encoder Representations from Transformers", "ResNet is also known as Residual Network", etc.
- is superior to: refers to a higher-level, more abstract or more general concept. In a knowledge graph or ontology, a superior concept may have one or more subordinate concepts that are more specific or concrete. For example, "language model" is superior to "BERT", "Transformer", etc.

The output should be a list of triple: (entity1, relation, entity2), where entity1 and entity2 are entities I provide, and relation is a DIRECTED relation between the two entities.

For example, if the summary is 
"BERT is a language model proposed by Google in 2018. It is based on the Transformer architecture.", 
and the entities are 
{{"type": "model", "name": "BERT", "description": "BERT is a language model proposed by Google in 2018"}}
{{"type": "model", "name": "Transformer", "description": "Transformer is a neural network architecture proposed by Google in 2017"}}
{{"type": "model", "name": "transformer", "description": "Transformer is a neural network architecture proposed by Google in 2017"}}
{{"type": "conception", "name": "language model", "description": "A language model is a model that can predict the next word given the previous words"}}

then the output should be:
(BERT, based_on, Transformer)
(Transformer, alias, transformer)
(language model, is superior to, BERT)
(network science, is superior to, small-world networks)

Note that the descriptions of relations should all come from the summary, and should be as biref as possible. You are not allowed to use external resources to add new descriptions. The DIRECTION of the relations matters! For example, (BERT, based_on, Transformer) is correct, but (Transformer, based_on, BERT) is wrong.

After generate the relations, you should check whether the relations are correct. If the relations are not correct, you should correct them and return the correct relations. If the relations are correct, you should return the relations directly.

Now let's get started!

The input summary is

{summary}

The input entities are

{entities}

The output relations are
"""