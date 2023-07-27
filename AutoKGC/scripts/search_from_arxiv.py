import argparse
import json

import arxiv
import yaml

from AutoKGC.tools.arxiv.base import dump_to_json, response_to_json
from AutoKGC.procedure.load_config import load_config

config = load_config()

# convert query as a argument
parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, required=True)
parser.add_argument('--max-results', type=int, default=4)
parser.add_argument('--data-path', type=str,
                    default=config['extractor']['arxiv']['data_path'])
args = parser.parse_args()

query = args.query
search = arxiv.Search(
    query=query,
    max_results=args.max_results,
    sort_by=arxiv.SortCriterion.Relevance,
    sort_order=arxiv.SortOrder.Descending
)
res = response_to_json(search)
dump_to_json(res, args.data_path, query.replace(' ', '_').replace('-', '_'))
