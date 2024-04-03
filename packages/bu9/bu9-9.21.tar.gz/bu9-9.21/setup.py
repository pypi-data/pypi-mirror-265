from setuptools import setup

setup(
    name='bu9',
    version='9.21',
    py_modules=['bu9'],
    entry_points={
        'console_scripts': [
            'bu9 = bu9:main',
        ],
    },
    install_requires=[],
)
