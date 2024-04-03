from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name = 'CalculyFy',
    version = '1.0',
    packages = find_packages(),
    requires = ['colorama'],
    entry_points = {
        "console_scripts" : [
            'clc-check = calculyfy.cli:check',
            'clc-info = calculyfy.cli:dist_info'
        ],
    },
    long_description = description,
    long_description_content_type = 'text/markdown'
)