def candidate_entities_warpper(candidate_entities: list[tuple]) -> str:
    prefix = "[\n"
    suffix = "\n]"
    content = ""
    for name, description in candidate_entities:
        content += f"""\t"{name}: {description}",\n"""
    return prefix + content[:-2] + suffix
if __name__ == "__main__":
    formated = candidate_entities_warpper([('Q1', 'A'), ('Q2', 'B')])
    print(formated)