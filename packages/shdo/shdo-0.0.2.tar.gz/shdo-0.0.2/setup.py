from setuptools import setup

setup(
    name='shdo',
    version='0.0.2',
    packages=['shdo'],
    package_dir={'shdo': '.'},
    py_modules=['shdo'],
    entry_points={
        'console_scripts': [
            'shdo = shdo:main'
        ]
    }
)