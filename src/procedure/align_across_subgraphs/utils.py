import json

def read_json_cases(file_path):
    with open(file_path, 'r') as f:
        id_pair_list = json.load(f)
    return id_pair_list

def parse_paper_id_piars(paper_id_pairs, db_manager):
    "input: id_pair which is a list of pairs of (paper_id_type, paper_id_value)"
    "output: a list of entities"
    res = db_manager.graph.query("""MATCH (n:Paper)
        WHERE
            n.title='Communicability Graph and Community Structures in Complex Networks'
            OR
            n.title='Transforming complex network to the acyclic one'
        MATCH (n)-[:EXTRACTED_FROM]-(other)
        RETURN n as paper, collect(other) as entities
    """)
    print(res[0]['paper'])
    print(len(res[0]['entities']))
    print(res[1]['paper'])
    print(len(res[1]['entities']))
def align_two_subgraphs(subgraph1, subgraph2):
    ...