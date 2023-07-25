def entities_warpper(candidate_entities: list[tuple], is_candiate=True) -> str:
    if not is_candiate:
        assert len(candidate_entities) == 1
        prefix = ""
        suffix = ""
    else:
        prefix = "[\n"
        suffix = "\n]"
    content = ""
    for name, description in candidate_entities:
        content += f"""\t"{name}: {description}",\n"""
    return prefix + content[:-2] + suffix
if __name__ == "__main__":
    formated = entities_warpper([('Q1', 'A'), ('Q2', 'B')])
    print(formated)