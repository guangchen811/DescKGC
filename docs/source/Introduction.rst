Introduction
============

procedures
----------
The procedures modules contain core workflows of AutoKGC.

- ``load_config`` - Loads AutoKGC configuration 
- ``extract_entity`` - Extracts entities from text
- ``search_arxiv`` - Searches Arxiv for relevant papers
- ``add_from_arxiv`` - Adds papers from Arxiv to the knowledge graph
- ``align_entities`` - Aligns extracted entities to existing nodes
- ``manage_db`` - Manages the underlying knowledge graph database

Scripts
-------

The scripts modules provide utility scripts.

- ``add_from_arxiv`` - Script to add papers from Arxiv
- ``align_entities`` - Script for aligning entities  
- ``extract_entity`` - Script for extracting entities
- ``manage_db`` - Database management script
- ``search_arxiv`` - Script to search Arxiv

Tests
-----

The tests modules contain test cases for AutoKGC.

- ``unit`` - Unit tests for components
- ``integration`` - Integration tests  
- ``end_to_end`` - End-to-end system tests

Tools
----- 

The tools modules provide supporting utilities.

- ``data`` - Data loading and preprocessing
- ``evaluation`` - Evaluation metrics and utilities
- ``models`` - Common ML model architectures