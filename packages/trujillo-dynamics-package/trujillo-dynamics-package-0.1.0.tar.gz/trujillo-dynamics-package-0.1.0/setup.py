from setuptools import setup, find_packages

readme = open("./README.md", "r", encoding="utf-8")

setup(
    name="trujillo-dynamics-package",
    version="0.1.0",
    packages=find_packages(),
    license="MIT",
    long_description=readme.read(),
    long_description_content_type="text/markdown; charset=UTF-8",
    description="Paquete que tiene como proposito el brindar clases de permitan realizar una conexión con data entities de Dynamics 365 Finance and Operations",
    author="Fernando Colque",
    install_requires=['pandas','requests','pathlib','azure.storage.blob'],
    author_email="fernando.colque@terranovatrading.com.pe",
)