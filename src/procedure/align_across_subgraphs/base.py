from .utils import (
    read_json_cases,
    parse_paper_id_pairs,
    cos_metric_between_sent_sets,
    add_sim_metric_to_db
)

if __name__ == '__main__':
    import os
    from transformers import logging
    logging.set_verbosity_error()
    from src.tools.neo4j.base import Neo4jManager
    from transformers import BertTokenizer, BertModel

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained("bert-base-uncased")

    db_manager = Neo4jManager()
    cur_path = os.path.dirname(__file__)
    id_pair_list = read_json_cases(f'{cur_path}/example_papers.json')
    papers_list, entities_list = parse_paper_id_pairs(id_pair_list, db_manager)
    cos_metric = cos_metric_between_sent_sets(entities_list[0], entities_list[1], tokenizer, model)
    print([entity['id'] for entity in entities_list[0]])
    add_sim_metric_to_db(db_manager, cos_metric, entities_list[0], entities_list[1])
    db_manager.close_driver()