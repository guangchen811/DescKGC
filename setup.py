from setuptools import find_packages, setup

setup(
    name='AutoKGC',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'argparse',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'manage-db=scripts.manage_db:main',
        ],
    },
)
