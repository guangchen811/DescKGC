import json
import torch
import torch.nn as nn

def tokenize_and_encode(sentences, tokenizer, model, max_batch_size=64, padding_length=128):
    """
    Tokenize and encode the sentences
    """
    encoded = []
    for i in range(0, len(sentences), max_batch_size):
        encoded_batch = tokenizer.batch_encode_plus(
            sentences[i : i + max_batch_size],
            padding="max_length",
            max_length=padding_length,
            truncation=True,
            return_tensors="pt",
        )
        # model outputs the last hidden states
        with torch.no_grad():
            model_output = model(**encoded_batch)
        batch_last_hidden_states = model_output.last_hidden_state
        encoded.append(batch_last_hidden_states.mean(dim=1))
    encoded = torch.cat(encoded, dim=0)
    return encoded

def cos_sim_between_sentences(sentence, sentences, tokenizer, model):
    encoded = tokenize_and_encode([sentence] + sentences, tokenizer, model)
    cos = nn.CosineSimilarity(dim=1, eps=1e-6)
    return cos(encoded[0].unsqueeze(0), encoded[1:])

def read_json_cases(file_path):
    with open(file_path, 'r') as f:
        id_pair_list = json.load(f)
    return id_pair_list