from setuptools import find_packages, setup

setup(
    name='AutoKGC',
    version='0.0.3',
    packages=find_packages(),
    readme="README.md",
    description='Automatic Knowledge Graph Construction',
    include_package_data=True,
    install_requires=[
        'argparse',
        'pyyaml',
        'chroma',
        'neo4j',
        'langchain',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'autokgc-add-from-arxiv=AutoKGC.scripts.main.add_from_arxiv:main',
            'autokgc-manage-db=AutoKGC.scripts.manage_db:main',
            'autokgc-entity-alignment=AutoKGC.scripts.entity_alignment:main',
            'autokgc-extract-entity-from-doc=AutoKGC.scripts.extract_entity_from_doc:main',
            'autokgc-search-from-arxiv=AutoKGC.scripts.search_from_arxiv:main',
        ],
    },
)
