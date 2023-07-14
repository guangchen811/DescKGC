import re
import argparse
from src.tools.neo4j.base import Neo4jManager

parser = argparse.ArgumentParser()
parser.add_argument('--delete-by-type', action='store_true')
parser.add_argument('--delete-all', action='store_true')
parser.add_argument('--show-schema', action='store_true')
args = parser.parse_args()

db_manager = Neo4jManager()
node_labels = db_manager.get_node_labels()


if args.delete_by_type:
    if len(node_labels) == 0:
        print('No data in the database.')
    else:
        type_name = input('The available types are: [' + ', '.join(node_labels) + '].' + '\nPlease input the type name: \n')
        db_manager.delete_by_type(type_name)
        print(f'Delete all nodes with type {type_name}.')

if args.delete_all:
    if len(node_labels) == 0:
        print('No data in the database.')
    else:
        confirmation = input('Are you sure to delete all data? (y/n): ')
        if confirmation == 'y':
            for node_label in node_labels:
                db_manager.delete_by_type(node_label)
        else:
            print('Delete aborted.')

if args.show_schema:
    db_manager.show_schema()