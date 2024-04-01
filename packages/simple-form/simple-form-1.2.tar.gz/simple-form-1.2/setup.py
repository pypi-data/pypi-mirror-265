import os
from setuptools import setup

if os.path.isfile("README.md"):
    with open("README.md", "r", encoding="utf-8") as readme:
        long_description = readme.read()

setup(
    name="simple-form",
    version=1.2,
    description="Pequena biblioteca para facilitar formulários em CLI com Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alan Reis Anjos",
    author_email="alanreisanjo@gmail.com",
    url="https://github.com/Hoyasumii/SimpleForm",
    packages=['simpleForm', 'simpleForm.scripts'],
    install_requires=['keyboard==0.13.5', 'setuptools==69.0.3'],
    license="GPL-3.0",
    entry_points={'console_scripts': []}
)
