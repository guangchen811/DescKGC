"""
This is a procedure to add data from arxiv to neo4j.
The complex_network.json is a result of arxiv search which is generated by src/tools/arxiv/base.py
"""
import json, yaml
import argparse
from pathlib import Path
from src.tools.db_manager.base import DBManager

with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser()
parser.add_argument('--data-path', type=str, default=config['extractor']['arxiv']['data_path'])
parser.add_argument('--file-name', type=str, required=True)
args = parser.parse_args()
# Load the json file
data_path = Path(args.data_path)
file_path = data_path / f"{args.file_name}.json"

# Initiate a neo4j manager
db_manager = DBManager()
# This function will add papers from arxiv to neo4j and extract authors from the paper.
# The author nodes will be connected to the paper nodes by "WROTE" relationship with a timestamp attribute.
print(f"adding data from {file_path}")
with open(file_path, 'r') as f:
    arxiv_papers = json.load(f)
db_manager.add_from_arxiv(arxiv_papers, arxiv_prefix=config['shortenings']['Paper'])