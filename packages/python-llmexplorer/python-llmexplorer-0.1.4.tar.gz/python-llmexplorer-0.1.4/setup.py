from setuptools import setup, find_packages

# Package metadata
NAME = 'python-llmexplorer'
VERSION = '0.1.4'
DESCRIPTION = 'A Tool that can be used to analyse, monitor prompts usage and LLM ops'
URL = 'https://github.com/9throok/LLMExplorer'
AUTHOR = 'The LLM Explorer Team'
EMAIL = ''
LICENSE = 'MIT'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.8',
]

# Package dependencies
INSTALL_REQUIRES = [
    'requests >=2.31.0',
    'openai >=1.0.0',
]

# Development dependencies
DEV_REQUIRES = [
    'fastapi',
    'elasticsearch',
]

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    keywords='LLMOps Prompting RAG',
    packages=find_packages("llmexplorer"),  #['llmexplorer'],
    install_requires=INSTALL_REQUIRES,
    python_requires='>=3.7',
    extras_require={
        'dev': DEV_REQUIRES,
    },
)
