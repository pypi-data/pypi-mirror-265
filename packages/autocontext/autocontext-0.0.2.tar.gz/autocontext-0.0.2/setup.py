import os
from pathlib import Path
from setuptools import setup, find_packages


setup(
    name='autocontext',
    version=os.getenv("GITHUB_REF_NAME"),
    author='George Haddad',
    description='a library to inject context related dependencies',
    long_description_content_type='text/markdown',
    long_description=Path('README.md', encoding='utf-8').read_text(),
    packages=find_packages(),
    include_package_data=True,
    license="Apache Software License (Apache 2.0)",
    keywords=[
        'python', 'autowired', 'autocontext', 'auto', 'context'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
    ]
)
