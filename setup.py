from setuptools import setup

setup(
    name='autokgc',
    entry_points={
        console_scripts: [
            'autokgc = autokgc.__main__:main'
        ]
    }
)