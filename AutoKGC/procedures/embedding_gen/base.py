from transformers import BertModel, BertTokenizer

from .utils import cos_sim_between_sentences, read_json_cases

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

if __name__ == "__main__":
    import os

    cur_path = os.path.dirname(__file__)
    summary_pair_list = read_json_cases(f"{cur_path}/example_sentences.json")
    summary_sentences = [pair["summary"] for pair in summary_pair_list]
    print(
        cos_sim_between_sentences(
            "network communicability", summary_sentences, tokenizer, model
        )
    )
    print(
        cos_sim_between_sentences(
            "complex network", summary_sentences, tokenizer, model
        )
    )
    print(
        cos_sim_between_sentences(
            "complex system", summary_sentences, tokenizer, model
        )
    )