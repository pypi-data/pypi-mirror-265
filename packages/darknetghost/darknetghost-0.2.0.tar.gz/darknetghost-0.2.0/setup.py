from setuptools import setup, find_packages 

#Leer el contenido del archivo README.md 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="darknetghost",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[],
    author="DarknetGhost",
    description="Biblioteca para consultar cursos de hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
