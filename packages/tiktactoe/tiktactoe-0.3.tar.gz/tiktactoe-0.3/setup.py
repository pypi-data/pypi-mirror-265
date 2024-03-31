from setuptools import setup, find_packages

setup(
    name='tiktactoe',
    version='0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tiktactoe=tiktactoe.main:main'
        ]
    },
    description='A simple Tic Tac Toe game',
    author='Aryan Mishra',
    author_email='aryanmishra101112@gmail.com',
)
