from setuptools import setup, find_packages

setup(
    name='zenfinal',
    version='0.2',
    packages=['zenfinal'],  # Explicitly specify the package
    package_dir={'zenfinal': 'zenfinal'},  # Specify the directory where the package files are located
    py_modules=['zenfinal'],
    entry_points={
        'console_scripts': [
            'hello = zenfinal.zenfinal:main'
        ]
    }
)