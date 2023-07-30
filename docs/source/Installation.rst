Installation
============

Prerequisites
-------------

Before installing AutoKGC, you need to install Neo4j first. The following are recommended install methods for different operating systems:

- Debian/Ubuntu: https://debian.neo4j.com/
- RedHat/CentOS: https://neo4j.com/docs/operations-manual/current/installation/linux/rpm/
- Windows: https://neo4j.com/docs/operations-manual/current/installation/windows/
- MacOS: https://neo4j.com/docs/operations-manual/current/installation/osx/
- Docker: https://neo4j.com/developer/docker-run-neo4j/

To be noticed, AutoKGC is developed and tested on `Neo4j 5.7.0`. It may not work on other versions.

Besides neo4j itself, you also need to install some neo4j plugins: APOC and GDS. If you are using Neo4j Desktop, you can install them by clicking the `Plugins` button on the left side of the window. If you are using other installation methods, you can install them by following the instructions on the official website:

- APOC: https://neo4j.com/labs/apoc/5/installation/
- GDS: https://neo4j.com/docs/graph-data-science/current/installation/

Install from Source
-------------------

Because AutoKGC is still under development, it is not open to the public yet. If you want to try it, please contact the author for the source code.

After downloading the source code, you can install it by running:

.. code-block:: bash

  pip install .