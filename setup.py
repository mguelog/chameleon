from setuptools import setup, find_packages

setup(
    name='chameleon',
    version='0.4.0',
    packages=find_packages(),
    url='https://github.com/mguelog/chameleon',
    author='Miguel Oña Guerrero',
    entry_points={
        "console_scripts": [
            "chameleon = chameleon.main:main",
        ]
    }
)
