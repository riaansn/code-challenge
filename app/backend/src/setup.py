from setuptools import setup

setup( 
    name='backend',
    version='0.1',
    author='Riaan Snyman',
    author_email='riaansnymansa@gmail.com',
    packages=['repositories', 'models'],
    entry_points={
        'console_scripts': [
            'backend = src.main:main'
        ]
    },)