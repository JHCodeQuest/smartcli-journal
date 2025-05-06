from setuptools import setup, find_packages

setup(
    name="cmdjournal",
    version="0.1",
   packages=find_packages(),
    install_requires=[
        "textblob",
    ],
    entry_points={
        "console_scripts": [
            "cmdjournal=cmdjournal.cmdjournal:controls",
        ],
    },
)