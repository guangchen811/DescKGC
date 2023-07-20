import yaml
import argparse
from src.tools.db_manager.base import DBManager
with open('./config.yaml', 'r') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

parser = argparse.ArgumentParser()
parser.add_argument('--entity_types', type=list)
args = parser.parse_args()