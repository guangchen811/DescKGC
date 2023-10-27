Installation
============

Prerequisites
-------------

Before installing DescKGC, you need to install Neo4j first. The following are recommended install methods for different operating systems:

- Debian/Ubuntu: https://debian.neo4j.com/
- RedHat/CentOS: https://neo4j.com/docs/operations-manual/current/installation/linux/rpm/
- Windows: https://neo4j.com/docs/operations-manual/current/installation/windows/
- MacOS: https://neo4j.com/docs/operations-manual/current/installation/osx/
- Docker: https://neo4j.com/developer/docker-run-neo4j/

To be noticed, DescKGC is developed and tested on `Neo4j 5.7.0`. It may not work on other versions.

Besides neo4j itself, you also need to install some neo4j plugins: APOC and GDS. If you are using Neo4j Desktop, you can install them by clicking the `Plugins` button on the left side of the window. If you are using other installation methods, you can install them by following the instructions on the official website:

- APOC: https://neo4j.com/labs/apoc/5/installation/
- GDS: https://neo4j.com/docs/graph-data-science/current/installation/

Install from Source
-------------------

DescKGC can be installed with pip.

.. code-block:: bash

  pip install desckgc

To test if the installation is successful, you can run:

.. code-block:: bash

  desckgc --help

The output should be like this:

.. code-block:: bash

  usage: desckgc [-h]
               {manage-db,search-from-arxiv,extract-entity-from-doc,add-from-arxiv,entity-alignment} ...

  DescKGC CLI

  positional arguments:
    {manage-db,search-from-arxiv,extract-entity-from-doc,add-from-arxiv,entity-alignment}
      manage-db           Monitors and manages the database.
      search-from-arxiv   Search papers from arXiv and dump them as json.
      extract-entity-from-doc
                          extract entities from documents in the database.
      add-from-arxiv      Add papers from local json files to databases.
      entity-alignment    Align entities in the database.

  optional arguments:
    -h, --help            show this help message and exit

If you can see this output, it means that you have successfully installed DescKGC. You can now use it to construct your own knowledge graph.