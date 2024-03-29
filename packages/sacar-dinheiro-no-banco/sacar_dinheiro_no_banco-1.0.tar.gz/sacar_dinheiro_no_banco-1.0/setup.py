from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='sacar_dinheiro_no_banco',
    version=1.0,
    description='Este pacote simula um login de uma pessoa que vai sacar dinheiro.',
    long_description=Path('README.md').read_text(),
    author='João Paulo',
    author_email='jpsampaiosampaio@gmail.com',
    keywords=['login', 'status', 'banco'],
    packages=find_packages()
)