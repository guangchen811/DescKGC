import json
import time
from ..embedding_gen.utils import cos_sim_between_sentences_sets
from typing import List


def read_json_cases(file_path):
    with open(file_path, 'r') as f:
        id_pair_list = json.load(f)
    return id_pair_list


def parse_paper_id_pairs(paper_id_pairs, db_manager):
    paper_shorten = 'p'
    paper_conditions = " or ".join(
        [f"{paper_shorten}.{k}='{v}'" for paper_id_pair in paper_id_pairs for k, v in paper_id_pair.items()])

    res = db_manager.graph.query(f"""MATCH ({paper_shorten}:Paper)
    WHERE {paper_conditions}
    MATCH ({paper_shorten})-[:EXTRACTED_FROM]-(other)
    RETURN {paper_shorten} as paper, collect({{entity: other, id: elementID(other)}}) as entities
    
    """)
    papers = [r['paper'] for r in res]
    entities = [r['entities'] for r in res]
    assert len(papers) == len(
        entities), f"len(papers)={len(papers)} != len(entities)={len(entities)}"

    # for i in range(len(res)):
    #     print(res[i]['paper'])
    #     print(res[i]['entities'][0])
    #     break
    #     # print(len(res[i]['entities']))
    return papers, entities


def cos_metric_between_sent_sets(set1: List[dict], set2: List[dict], tokenizer, model, **kwargs) -> None:
    """Align two subgraphs by adding relations between entities in the two subgraphs."""
    sentences_set1 = [entity['entity']['description'] for entity in set1]
    sentences_set2 = [entity['entity']['description'] for entity in set2]
    sim_metrics = cos_sim_between_sentences_sets(sentences_set1, sentences_set2,
                                                 tokenizer, model, **kwargs)
    return sim_metrics


def add_sim_metric_to_db(db_manager, cos_metric, set1, set2):
    current_time = time.localtime()
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    for i, entity1 in enumerate(set1):
        for j, entity2 in enumerate(set2):
            db_manager.graph.query(f"""MATCH (e1)
            WHERE elementID(e1)='{entity1['id']}'
            MATCH (e2)
            WHERE elementID(e2)='{entity2['id']}'
            MERGE (e1)-[r:SIMILARITY]-(e2)
            SET r.cos_metric={cos_metric[i, j].item()}
            SET r.timestep='{time_str}'
            """)
