import argparse

from AutoKGC.scripts import add_from_arxiv, entity_alignment, extract_entity_from_doc, manage_db, search_from_arxiv


def main():
    parser = argparse.ArgumentParser(description="AutoKGC CLI")
    subparsers = parser.add_subparsers(dest="command")

    module_manage_db = subparsers.add_parser("manage-db", help="Monitors and manages the database.")
    manage_db.add_arguments(module_manage_db)
    module_manage_db.set_defaults(func=manage_db.main)

    module_search_from_arxiv = subparsers.add_parser(
        "search-from-arxiv", help="Search papers from arXiv and dump them as json."
    )
    search_from_arxiv.add_arguments(module_search_from_arxiv)
    module_search_from_arxiv.set_defaults(func=search_from_arxiv.main)

    module_extract_entity_from_doc = subparsers.add_parser(
        "extract-entity-from-doc", help="extract entities from documents in the database."
    )
    extract_entity_from_doc.add_arguments(module_extract_entity_from_doc)
    module_extract_entity_from_doc.set_defaults(func=extract_entity_from_doc.main)

    module_add_from_arxiv = subparsers.add_parser("add-from-arxiv", help="Add papers from local json files to databases.")
    add_from_arxiv.add_arguments(module_add_from_arxiv)
    module_add_from_arxiv.set_defaults(func=add_from_arxiv.main)

    module_entity_alignment = subparsers.add_parser("entity-alignment", help="Align entities in the database.")
    entity_alignment.add_arguments(module_entity_alignment)
    module_entity_alignment.set_defaults(func=entity_alignment.main)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


if __name__ == "__main__":
    main()
