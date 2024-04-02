from setuptools import setup, find_packages

setup(
    name='zenfinal',
    version='0.1',
    packages=find_packages(),
    py_modules=['zenfinal'],
    entry_points={
        'console_scripts': [
            'zenfin = zenfinal.zenfinal:main'
        ]
    }
)
