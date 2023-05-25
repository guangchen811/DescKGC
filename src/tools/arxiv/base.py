# should be format, but not yet.
import arxiv
import json

def response_to_json(search_res):
    res = []
    for result in search_res.results():
        res.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "published": result.published,
            "updatedDate": result.updated,
            "summary": result.summary,
            "doi": result.doi,
            "primary_category": result.primary_category,
            "categories": result.categories,
            "pdf_url": result.pdf_url,
        })
    print(result.authors)
    return res
def dump_to_json(res, dir_path, file_name):
    file_path = dir_path + file_name + '.json'
    with open(file_path, 'w') as f:
        json.dump(res, f)
    

if __name__ == '__main__':
    query = "network science"
    search = arxiv.Search(
        query = query,
        max_results = 1,
        sort_by = arxiv.SortCriterion.Relevance,
        sort_order = arxiv.SortOrder.Descending
    )
    res = response_to_json(search)
    print(res)
    # dump_to_json(res, './data/', query.replace(' ', '_'))