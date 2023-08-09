from setuptools import find_packages, setup

setup(
    name='AutoKGC',
    version='0.0.3',
    packages=find_packages(),
    readme="README.md",
    description='Automatic Knowledge Graph Construction',
    include_package_data=True,
    package_data={
        'AutoKGC': ['.kgc_config.yaml']
    },
    install_requires=[
        'argparse',
        'pyyaml',
        'chroma',
        'neo4j',
        'langchain',
        'tqdm',
        'pydantic==1.10.8',
    ],
    entry_points={
        'console_scripts': [
            'autokgc=AutoKGC.scripts.cli:main'
        ],
    },
)
