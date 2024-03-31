from setuptools import setup, find_packages

setup(
    name='osonfom',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'osonfom=mytictactoe:main'
        ]
    },
    description='A simple Tic Tac Toe game',
    author='Aryan Mishra',
    author_email='aryanmishra101112@gmail.com',
)
