from setuptools import setup, find_packages

setup(
    name='hw2latex',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'imagelatex=two:imagelatex',
            'generate_latex_table = two:generate_latex_table'
        ],
    },
)
