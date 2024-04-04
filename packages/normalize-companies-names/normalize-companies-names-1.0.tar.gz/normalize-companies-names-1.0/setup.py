from setuptools import setup, find_packages

setup(
    name='normalize-companies-names',
    version='1.0',
    author='Willerson Abreu',
    author_email='willersonabreu@hotmail.com',
    description='A custom Python library to add new column with normalized companies names under a new column on Excel file',
    packages=find_packages(),
    install_requires=[
        "click",
        "thefuzz",
        "pandas",
        "openpyxl"
    ],
    entry_points={
        'console_scripts': [
            'normalize = src.main:main'
        ]
    }
)
