ARXIV_PAPER_INSERT_INSTRUCTION = """MERGE (:Paper {{title: "{title}", authors: "{authors}", published: "{published}", updatedDate: "{updatedDate}", summary: "{summary}", doi: "{doi}", primary_category: "{primary_category}", categories: "{categories}", pdf_url: "{pdf_url}"}})
"""

DELETE_NODES_INSTRUCTION = """MATCH (n:{type})
DELETE n"""