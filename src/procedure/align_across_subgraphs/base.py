from .utils import (
    read_json_cases,
    parse_paper_id_piars,
    align_two_subgraphs
)



if __name__ == '__main__':
    import os
    from src.tools.neo4j.base import Neo4jManager
    
    db_manager = Neo4jManager()
    cur_path = os.path.dirname(__file__)
    id_pair_list = read_json_cases(f'{cur_path}/example_papers.json')
    parse_paper_id_piars(id_pair_list, db_manager)