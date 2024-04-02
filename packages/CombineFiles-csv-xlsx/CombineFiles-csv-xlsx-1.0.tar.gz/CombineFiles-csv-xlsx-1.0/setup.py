from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open('readme.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CombineFiles-csv-xlsx',
    version='1.0',
    packages=find_packages(),
    install_requires=['pandas'],
    author='Omkar Sutar',
    author_email='Omkarsutar9702@gmail.com',
    description='Python package to combine multiple Excel and CSV files in a folder.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
