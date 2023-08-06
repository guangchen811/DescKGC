from typing import List, Tuple


def entities_nd_pair_warpper(candidate_entities: List[tuple], is_candiate=True) -> str:
    """Wrap the candidate entities into a string.
    The input is a list of tuples, each tuple contains the name and the description of the entity.
    :param candidate_entities: The candidate entities
    :type candidate_entities: list[tuple]
    :param is_candiate: Whether the candidate entities are the source entity, defaults to True
    :type is_candiate: bool, optional
    :return: The wrapped string
    :rtype: str
    """
    if not is_candiate:
        assert len(candidate_entities) == 1
        prefix = ""
        suffix = ""
    else:
        if len(candidate_entities) == 0:
            return "[]"
        prefix = "[\n"
        suffix = "\n]"
    content = ""
    for name, description in candidate_entities:
        content += f"""\t"{name}: {description}",\n"""
    return prefix + content[:-2] + suffix


def entities_ndg_pair_warpper(candidate_entities: List[Tuple[str, str, bool]], is_candidate=True) -> str:
    """Wrap the candidate entities into a string.
    The input is a list of tuples, each tuple contains the name, the description and generalbility of the entity.
    :param candidate_entities: The candidate entities
    :type candidate_entities: list[tuple]
    :param is_candiate: Whether the candidate entities are the source entity, defaults to True
    :type is_candiate: bool, optional
    """
    if not is_candidate:
        raise NotImplementedError
    else:
        if len(candidate_entities) == 0:
            return "[]"
        prefix = "[\n"
        suffix = "\n]"
    content = ""
    for name, description, generalbility in candidate_entities:
        content += f"""\t"{name}": "{description}" """
        content += f""" generalbility: {generalbility},\n"""
    return prefix + content[:-2] + suffix


if __name__ == "__main__":
    formated_nd = entities_nd_pair_warpper([("Q1", "A"), ("Q2", "B")])
    format_ndg = entities_ndg_pair_warpper([("Q1", "A", True), ("Q2", "B", False)])
    print(formated_nd)
    print(format_ndg)
