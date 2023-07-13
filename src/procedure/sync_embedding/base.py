import uuid

def generate_node_id(node_type):
    node_prefix = get_node_prefix(node_type)
    unique_id = str(uuid.uuid4())
    node_id = f"{node_prefix}{unique_id}"
    return node_id

def get_node_prefix(node_type):
    prefixes = {
        'paper': 'P',
        'concept': 'C',
        'dataset': 'D',
    }
    return prefixes.get(node_type.lower(), '')

# Example usage
paper_node_id = generate_node_id('paper')
print(paper_node_id)