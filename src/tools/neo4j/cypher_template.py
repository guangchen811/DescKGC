ARXIV_PAPER_INSERT_INSTRUCTION = """MERGE (:Paper {{title: "{title}", authors: "{authors}", published: "{published}", updatedDate: "{updatedDate}", summary: "{summary}", doi: "{doi}", primary_category: "{primary_category}", categories: "{categories}", pdf_url: "{pdf_url}", uuid: "{uuid}"}})"""

DELETE_NODES_INSTRUCTION = """MATCH (n:{type})
DETACH DELETE n"""

DETACH_AUTHOR_FROM_PAPER_INSTRUCTION = """
match (p:Paper)
WITH p, split(p.authors, '||') AS authors
UNWIND authors as author
MERGE (a:Author {name: author})
MERGE (a)-[r:WROTE {timestep:p.published}]->(p)
"""