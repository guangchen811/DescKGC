# scripts/add_from_arxiv.py

import argparse
import json
from pathlib import Path

import yaml

from src.tools.db_manager.base import DBManager


def main(data_path, file_name):
    # Load the json file
    data_path = Path(data_path)
    file_path = data_path / f"{file_name}.json"

    # Initiate a neo4j manager
    db_manager = DBManager(**config['neo4jdb'], **config['chromadb'])
    # This function will add papers from arxiv to neo4j and extract authors from the paper.
    # The author nodes will be connected to the paper nodes by "WROTE" relationship with a timestamp attribute.
    print(f"adding data from {file_path}")
    with open(file_path, 'r') as f:
        arxiv_papers = json.load(f)
    db_manager.add_from_arxiv(
        arxiv_papers,
        arxiv_prefix=config['shortenings']['Paper'],
        vs_key_info=config['extractor']['arxiv']['vs_key_info']
    )


if __name__ == "__main__":
    with open('./config.yaml', 'r') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    parser = argparse.ArgumentParser()
    parser.add_argument('--data-path', type=str,
                        default=config['extractor']['arxiv']['data_path'])
    parser.add_argument('--file-name', type=str, required=True)
    args = parser.parse_args()
    main(args.data_path, args.file_name)
