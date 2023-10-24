from dataclasses import dataclass
from typing import List, Type


@dataclass
class AriXivData:
    title: str
    authors: List[str]
    published: str
    updated_date: str
    summary: str
    doi: str
    primary_category: str
    categories: List[str]
    pdf_url: str


AriXivDataType = Type[AriXivData]
