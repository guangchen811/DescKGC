from DescKGC.tools.config_manager import ConfigManager


def load_config():
    """Load configuration file from the current directory.
    Currently, the configuration file is named as `.kgc_config.yaml`.
    """
    config_manager = ConfigManager()
    config = config_manager.get_config()
    return config
