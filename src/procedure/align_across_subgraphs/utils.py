import json

def read_json_cases(file_path):
    with open(file_path, 'r') as f:
        id_pair_list = json.load(f)
    return id_pair_list

def parse_paper_id_pairs(paper_id_pairs, db_manager):
    paper_shorten = 'p'
    paper_conditions = " or ".join([f"{paper_shorten}.{k}='{v}'" for paper_id_pair in paper_id_pairs for k, v in paper_id_pair.items()])
    "input: id_pair which is a list of pairs of (paper_id_type, paper_id_value)"
    "output: a list of entities"
    res = db_manager.graph.query(f"""MATCH ({paper_shorten}:Paper)
    WHERE {paper_conditions}
    MATCH ({paper_shorten})-[:EXTRACTED_FROM]-(other)
    RETURN {paper_shorten} as paper, collect(other) as entities
    """)
    for i in range(len(res)):
        print(res[i]['paper'])
        print(len(res[i]['entities']))
    return res
def align_two_subgraphs(subgraph1, subgraph2):
    ...