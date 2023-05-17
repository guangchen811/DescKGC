import json

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        train_lines = [json.loads(line) for line in f.readlines()]
        idx_type_dict = {idx: line['cate'] for idx, line in enumerate(train_lines)}
        type_idx_dict = {line['cate']: idx for idx, line in enumerate(train_lines)}
        for idx, _ in enumerate(train_lines):
            train_lines[idx]['required_relations'] = train_lines[idx]['instruction'].split('：')[1].split('，')[0]
        return train_lines, idx_type_dict, type_idx_dict
if __name__ == '__main__':
    path = '../../data/train.json'
    train_lines, idx_type_dict, type_idx_dict = load_json(path)
    aline = train_lines[0]
    cate = aline['cate']
    description = aline['input']
    required_relations = aline['required_relations']
    print("cate:", cate)
    print("description:", description)
    print("required_relations:", required_relations)