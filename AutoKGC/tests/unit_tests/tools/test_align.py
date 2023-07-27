from AutoKGC.tools.align.utils import entities_warpper


def test_entities_wrapper_with_candidates():
    candidate_entities = [("entity1", "description1"), ("entity2", "description2")]
    expected_result = '[\n\t"entity1: description1",\n\t"entity2: description2"\n]'
    assert entities_warpper(candidate_entities) == expected_result


def test_entities_wrapper_with_empty_candidate():
    candidate_entities = []
    expected_result = "[]"
    assert entities_warpper(candidate_entities) == expected_result


def test_entities_wrapper_with_multiple_candidates():
    candidate_entities = [("entity1", "description1"), ("entity2", "description2"), ("entity3", "description3")]
    expected_result = '[\n\t"entity1: description1",\n\t"entity2: description2",\n\t"entity3: description3"\n]'
    assert entities_warpper(candidate_entities) == expected_result


def test_entities_wrapper_with_special_characters():
    candidate_entities = [("entity1", "desc,ription1"), ("entity2", "descriptio\nn2")]
    expected_result = '[\n\t"entity1: desc,ription1",\n\t"entity2: descriptio\nn2"\n]'
    assert entities_warpper(candidate_entities) == expected_result
