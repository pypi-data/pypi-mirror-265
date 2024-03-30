from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='dilipred',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dilipred = dilipred.main:main',
        ],
        },
    install_requires=[
        line.strip() for line in open('requirements.txt') if line.strip()
    ],
    description="DILIPRedictor is an open-source app framework built specifically for human drug-induced liver injury",
    long_description=long_description,
    long_description_content_type="text/markdown",
)