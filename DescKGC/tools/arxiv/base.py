import dataclasses
import json

from .arxiv_data import AriXivData, AriXivDataType, List


def response_to_dataclass(search_res) -> List[AriXivDataType]:
    res = []
    for result in search_res.results():
        search_result = AriXivData(
            title=result.title,
            authors=[author.name for author in result.authors],
            published=str(result.published),
            updated_date=str(result.updated),
            summary=result.summary,
            doi=result.doi,
            primary_category=result.primary_category,
            categories=result.categories,
            pdf_url=result.pdf_url,
        )
        res.append(search_result)
    return res


def dump_to_json(res: List[AriXivDataType], dir_path: str, file_name: str):
    file_path = dir_path + file_name + ".json"
    with open(file_path, "w") as f:
        json.dump([dataclasses.asdict(item) for item in res], f)
