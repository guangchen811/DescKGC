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
            'autokgc=AutoKGC.scripts.cli:main'
        ],
    },
)
