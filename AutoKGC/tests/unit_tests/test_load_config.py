import os

import pytest
import yaml

from AutoKGC.procedures.load_config import load_config


def test_load_config_success(tmp_path):
    config_file = tmp_path / ".kgc_config.yaml"
    config_data = {"key": "value"}
    with open(config_file, "w") as f:
        yaml.safe_dump(config_data, f)

    os.chdir(tmp_path)  # change working directory to tmp_path
    assert load_config() == config_data


def test_load_config_failure(tmp_path):
    os.chdir(tmp_path)  # change working directory to tmp_path

    with pytest.raises(FileNotFoundError):
        load_config()
