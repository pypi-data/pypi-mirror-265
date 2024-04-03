from setuptools import setup, find_packages

setup(
    name='booookscore',
    version='0.1.3',
    description='Official package for our ICLR 2024 paper, "BooookScore: A systematic exploration of book-length summarization in the era of LLMs".',
    author='Yapei Chang',
    author_email='yapeichang@umass.edu',
    url='https://github.com/lilakk/BooookScore',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'anthropic==0.21.3',
        'fire==0.5.0',
        'nltk==3.8.1',
        'numpy==1.23.1',
        'openai==1.16.1',
        'scripts==3.0',
        'setuptools==68.2.0',
        'tiktoken==0.5.2',
        'torch==1.13.1',
        'tqdm==4.66.1',
        'transformers==4.37.2',
    ]
)