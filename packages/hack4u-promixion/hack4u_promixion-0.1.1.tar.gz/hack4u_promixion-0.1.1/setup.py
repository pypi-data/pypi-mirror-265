from setuptools import setup, find_packages

#Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u_promixion",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[],
    author="Promixion",
    description="Biblioteca para consultar cursos de la academia hack4u.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io/",
)

