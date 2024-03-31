from setuptools import setup, find_packages
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
# Explicitly specify encoding as UTF-8
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='goodgit',
    version='0.1.32',
    packages=find_packages(),
    description='Git; for humans',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Shubham Gupta • Saket Gupta',
    author_email='shubhastro2@gmail.com',
    install_requires=[
        'requests',
        'GitPython',
        'questionary',
        'rich',
        'docopt',
        'halo',
        'remote-log',
    ],
    entry_points={
        'console_scripts': [
            'gg = goodgit.goodgit:main',
            'goodgit = goodgit.goodgit:main',
        ],
    },
)
