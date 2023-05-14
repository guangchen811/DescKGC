# should be format, but not yet.
import arxiv
import json

search = arxiv.Search(
    query = "network science",
    max_results = 100,
    sort_by = arxiv.SortCriterion.Relevance,
    sort_order = arxiv.SortOrder.Descending
)
def search_res_to_json(search_res):
    res = []
    for result in search_res.results():
        res.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "categories": result.categories,
            "summary": result.summary
        })
    return res
def write_json(res):
    with open('./data/arxiv_network_science.json', 'w') as f:
        json.dump(res, f)

res = search_res_to_json(search)
write_json(res)