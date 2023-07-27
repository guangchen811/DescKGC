import os

import yaml


def load_config():
    config_file = './.kgc_config.yaml'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    else:
        raise FileNotFoundError(
            f"Configuration file '{config_file}' not found."
            "Please ensure the file exists.")


if __name__ == "__main__":
    config = load_config()
    print(config)
