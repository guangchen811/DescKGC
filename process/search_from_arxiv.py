import arxiv
import json
from src.tools.arxiv.base import response_to_json, dump_to_json
import argparse

# convert query as a argument
parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, required=True)
parser.add_argument('--max-results', type=int, default=10)
args = parser.parse_args()

query = args.query
search = arxiv.Search(
    query = query,
    max_results = args.max_results,
    sort_by = arxiv.SortCriterion.Relevance,
    sort_order = arxiv.SortOrder.Descending
)
res = response_to_json(search)
dump_to_json(res, './data/', query.replace(' ', '_'))