import json
import time
from ..embedding_gen.utils import cos_sim_between_sentences_sets

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
    papers = [r['paper'] for r in res]
    entities = [r['entities'] for r in res]
    assert len(papers) == len(entities), f"len(papers)={len(papers)} != len(entities)={len(entities)}"
    # for i in range(len(res)):
    #     print(res[i]['paper'])
    #     print(res[i]['entities'][0])
    #     break
    #     # print(len(res[i]['entities']))
    return papers, entities

def cos_metric_between_sent_sets(set1: list[dict], set2: list[dict], tokenizer, model, **kwargs) -> None:
    """Align two subgraphs by adding relations between entities in the two subgraphs."""
    sentences_set1 = [entity['description'] for entity in set1]
    sentences_set2 = [entity['description'] for entity in set2]
    sim_metrics = cos_sim_between_sentences_sets(sentences_set1, sentences_set2, 
    tokenizer, model, **kwargs)
    return sim_metrics