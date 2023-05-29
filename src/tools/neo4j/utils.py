from typing import List, Union

def response_to_json(search_res):
    res = []
    for result in search_res.results():
        res.append({
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "published": str(result.published),
            "updatedDate": str(result.updated),
            "summary": result.summary,
            "doi": result.doi,
            "primary_category": result.primary_category,
            "categories": result.categories,
            "pdf_url": result.pdf_url,
        })
    return res

def join_if_list(input: Union[List[str], str, int]) -> str:
        if isinstance(input, list):
            return "||".join(input)
        else:
            return str(input)