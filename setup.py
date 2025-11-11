#!/usr/bin/env python3
"""
Setup script for Oracle SQL Formatter
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ''

setup(
    name='oracle-sql-formatter',
    version='1.0.0',
    description='Oracle SQL Formatter for DBeaver',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/oracle-sql-formatter',
    py_modules=['sql_formatter'],
    install_requires=[
        'sqlparse>=0.4.4',
        'PyYAML>=6.0',
    ],
    entry_points={
        'console_scripts': [
            'sql-formatter=sql_formatter:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
)
