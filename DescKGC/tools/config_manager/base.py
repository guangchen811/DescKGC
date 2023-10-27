from collections import OrderedDict

import oyaml as yaml

from .default_config import DescKGCConfig


class ConfigManager:
    def __init__(self, local_config_path=".kgc_config.yaml", default_config=DescKGCConfig(), verbose=False):
        self.local_config_path = local_config_path
        self.default_config = default_config

    def get_config(self):
        local_config = self._get_local_config(self.local_config_path)
        merged_config = DescKGCConfig(**local_config)
        # return ordered dict
        return merged_config.dict()

    def _convert_to_ordered_dict(self, config):
        if isinstance(config, dict):
            return OrderedDict([(key, self._convert_to_ordered_dict(value)) for key, value in config.items()])
        elif isinstance(config, list):
            return [self._convert_to_ordered_dict(value) for value in config]
        else:
            return config

    def _get_local_config(self, local_config_path):
        local_config = self._load_local_config(local_config_path)
        if local_config is None:
            print(
                "No local config found, use default config. "
                "Please run `desckgc manage-config --init` to initialize a local config."
            )
            exit(1)
        return local_config

    def init_local_config(self):
        local_config = self._load_local_config(self.local_config_path)
        if local_config is None:
            yaml.dump(self.default_config.dict(), open(self.local_config_path, "w"))
        else:
            print("Local config already exists, skip initialization.")

    def _load_local_config(self, local_config_path):
        try:
            with open(local_config_path, "r") as local_config_file:
                local_config = yaml.safe_load(local_config_file)
        except FileNotFoundError:
            local_config = None
        return local_config
