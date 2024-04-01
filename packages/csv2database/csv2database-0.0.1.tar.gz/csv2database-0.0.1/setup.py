from setuptools import setup, find_packages

setup(
    name='csv2database',
    version='0.0.1',
    author='Md Arfaan Baig',
    author_email='mdarfaanbaig@gmail.com',
    description='A package for importing CSV files into a MySQL database',
    long_description='This package provides functionality to import CSV files into a MySQL database, supporting both local and Google Drive sources.',
    url='https://github.com/mdarfaanbaig/csv2database',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'numpy>=1.0.0',
        'pandas>=1.0.0',
        'mysql-connector-python>=8.0.0',
        'google-api-python-client>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'csv_import=csv2database.main:main',
        ],
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
