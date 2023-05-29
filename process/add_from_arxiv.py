"""
This is an example of how to add data from arxiv to neo4j.
The complex_network.json is a result of arxiv search which is generated by src/tools/arxiv/base.py
"""

import json
from src.tools.neo4j.base import Neo4jManager
# Load the json file
with open('./data/complex_network.json', 'r') as f:
    res = json.load(f)
# Initiate a neo4j manager
db_manager = Neo4jManager()
# This function will add papers from arxiv to neo4j and extract authors from the paper.
# The author nodes will be connected to the paper nodes by "WROTE" relationship with a timestamp attribute.
db_manager.add_from_arxiv(res)