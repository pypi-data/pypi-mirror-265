from setuptools import setup, find_packages

setup(
name="qlatent",
author="cnlabs",
url="https://github.anonymos/",
author_email="cnlabs@anonymos.com",
version="1.0.0",
description="A Python package for running psychometric on LLMs.",
packages=find_packages(
        where=".",
        exclude=['data', 'qmnli','docs'],  # ['*'] by default
    ),
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: Apache Software License",
"Operating System :: OS Independent",
],
include_package_data=True,
python_requires=">=3.8",
install_requires=[
   'torch',
   'pandas',
   'numpy',
   'transformers',
   'scipy',
   'tqdm',
   'scipy',
   'typeguard',
   'sentence_transformers',
   'overrides',
   'altair',
   'scikit-learn',
   'datasets',
   'matplotlib',
   'typing',
   'pingouin',
],
)
