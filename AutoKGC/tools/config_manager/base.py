import yaml

from .default_config import AutoKGCConfig


class ConfigManager:
    def __init__(self, local_config_path=".kgc_config.yaml", default_config=AutoKGCConfig(), verbose=False):
        self.local_config_path = local_config_path
        self.default_config = default_config

    def get_config(self):
        local_config = self._get_local_config(self.local_config_path)
        merged_config = AutoKGCConfig(**local_config)
        return merged_config.dict()

    def _get_local_config(self, local_config_path):
        local_config = self._load_local_config(local_config_path)
        if local_config is None:
            print("No local config found, use default config. Please run `autokgc config init` to initialize a local config.")
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


if __name__ == "__main__":
    config_manager = ConfigManager()
    config_manager.init_local_config()
