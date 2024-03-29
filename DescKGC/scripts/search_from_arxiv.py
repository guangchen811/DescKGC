import argparse

import arxiv

from DescKGC.procedures.build_config import load_config
from DescKGC.tools.arxiv.base import dump_to_json, response_to_dataclass


def add_arguments(parser):
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--max-results", type=int, default=4)
    parser.add_argument("--data-path", type=str)


def main(args):
    config = load_config()
    # convert query as a argument
    query = args.query
    max_results = args.max_results
    if args.data_path is None:
        data_path = config["extractor"]["arxiv"]["data_path"]
    else:
        data_path = args.data_path
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )
    res = response_to_dataclass(search)
    dumped_file_name = query.replace(" ", "_").replace("-", "_")
    dump_to_json(res, data_path, dumped_file_name)
    print(f"dumped to {data_path} as {dumped_file_name}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    main(args)
