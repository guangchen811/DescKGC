from setuptools import find_packages, setup

setup(
    name='AutoKGC',
    version='0.0.1',
    packages=find_packages(),
    readme = "README.md",
    description='Automatic Knowledge Graph Construction',
    include_package_data=True,
    install_requires=[
        'argparse',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'manage-db=src.scripts.manage_db:main',
        ],
    },
)
