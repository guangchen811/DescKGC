import argparse

import arxiv

from AutoKGC.procedures.load_config import load_config
from AutoKGC.tools.arxiv.base import dump_to_json, response_to_json


def main(query, max_results, data_path):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    )
    res = response_to_json(search)
    dump_to_json(res, data_path, query.replace(" ", "_").replace("-", "_"))


if __name__ == "__main__":
    config = load_config()

    # convert query as a argument
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, required=True)
    parser.add_argument("--max-results", type=int, default=4)
    parser.add_argument("--data-path", type=str, default=config["extractor"]["arxiv"]["data_path"])
    args = parser.parse_args()

    main(args.query, args.max_results, args.data_path)
