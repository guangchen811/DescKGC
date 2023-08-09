import argparse
import json
from pathlib import Path

from AutoKGC.procedures.build_config import load_config
from AutoKGC.tools.db_manager import DBManager


def add_arguments(parser):
    parser.add_argument("--data-path", type=str)
    parser.add_argument("--file-name", type=str, required=True)


def main(args):
    config = load_config()
    if args.data_path is None:
        data_path = config["extractor"]["arxiv"]["data_path"]
    else:
        data_path = args.data_path
    file_name = args.file_name

    # Load the json file
    data_path = Path(data_path)
    file_path = data_path / f"{file_name}.json"

    # Initiate a neo4j manager
    db_manager = DBManager(**config["neo4jdb"], **config["chromadb"])
    # This function will add papers from arxiv to neo4j
    # and extract authors from the paper.
    # The author nodes will be connected to the paper nodes
    # by "WROTE" relationship with a timestamp attribute.
    print(f"adding data from {file_path}")
    with open(file_path, "r") as f:
        arxiv_papers = json.load(f)
    db_manager.add_from_arxiv(
        arxiv_papers,
        arxiv_prefix=config["shortenings"]["Paper"],
        vs_key_info=config["extractor"]["arxiv"]["vs_key_info"],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
