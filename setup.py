from setuptools import setup, find_packages

setup(
    name="wordlesolver",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "kivy",
        "kivymd",
        "pyjnius",
    ],
)