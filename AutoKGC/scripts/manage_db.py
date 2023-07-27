import argparse

from AutoKGC.procedures.load_config import load_config
from AutoKGC.tools.db_manager.base import DBManager


def main(args, config):
    db_manager = DBManager(**config["neo4jdb"], **config["chromadb"])
    node_labels = db_manager.get_node_labels()

    if args.delete_by_type:
        delete_by_type(db_manager, node_labels)

    if args.delete_all:
        delete_all(db_manager, node_labels)

    if args.show_schema:
        show_schema(db_manager)


def show_schema(db_manager):
    db_manager.show_schema()


def delete_all(db_manager, node_labels):
    if len(node_labels) == 0:
        print("No data in the database.")
    else:
        confirmation = input("Are you sure to delete all data? (y/n): ")
        if confirmation == "y":
            for node_label in node_labels:
                db_manager.delete_by_type(node_label)
            db_manager.vector_store.client.reset()
        else:
            print("Delete aborted.")


def delete_by_type(db_manager, node_labels):
    if len(node_labels) == 0:
        print("No data in the database.")
    else:
        print("The available types are:", end=" ")
        print(f'{", ".join(node_labels)}.')
        type_name = input("Please input the type name: \n")
        db_manager.delete_by_type(type_name)
        print(f"Delete all nodes with type {type_name}.")


if __name__ == "__main__":
    config = load_config()

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--delete-by-type",
        action="store_true",
        help="Delete nodes by type. You will be asked to enter the type.",
    )
    group.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete all nodes. You will be asked to confirm.",
    )
    group.add_argument(
        "--show-schema",
        action="store_true",
        help="Show the schema of the database.",
    )
    args = parser.parse_args()
    main(args, config)
