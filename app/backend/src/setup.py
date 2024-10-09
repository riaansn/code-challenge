from setuptools import setup

setup( 
    name='backend',
    version='0.1',
    packages=['repositories', 'models'],
    entry_points={
        'console_scripts': [
            'backend = app.backend.src.main:main'
        ]
    },)