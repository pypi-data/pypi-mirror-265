from __future__ import annotations

import bober
from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


def requirements() -> list[str]:
    with open('requirements.txt', 'r') as f:
        return f.read().splitlines()


setup(
    name='bober',
    version=bober.__version__,
    author='wristylotus',
    author_email='wristylotus@gmail.com',
    description='Tool to manage your jobs',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/wristylotus/Bober',
    packages=find_packages(),
    install_requires=requirements(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='bober job manager structure',
    project_urls={
        'Documentation': 'https://github.com/wristylotus/Bober/blob/main/README.md'
    },
    python_requires='>=3.8'
)
