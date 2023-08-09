import os

# import pkg_resources
import yaml

# config_file = pkg_resources.resource_filename("AutoKGC", ".kgc_config.yaml")
# print(config_file)
# with open(config_file, "r") as f:
#     config = yaml.safe_load(f)


def load_config():
    # TODO: complete this module
    """Load configuration file from the current directory.
    Currently, the configuration file is named as `.kgc_config.yaml`.

    :raises FileNotFoundError: If the configuration file is not found.
    """
    config_file = ".kgc_config.yaml"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        return config
    else:
        raise FileNotFoundError(f"Configuration file '{config_file}' not found." "Please ensure the file exists.")
