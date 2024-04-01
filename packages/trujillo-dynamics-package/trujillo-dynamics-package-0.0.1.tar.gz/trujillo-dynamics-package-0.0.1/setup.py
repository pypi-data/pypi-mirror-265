from setuptools import setup, find_packages


setup(
    name="trujillo-dynamics-package",
    version="0.0.1",
    packages=find_packages(),
    license="MIT",
    description="Paquete que tiene como proposito el brindar clases de permitan realizar una conexión con data entities de Dynamics 365 Finance and Operations",
    author="Fernando Colque",
    install_requires=['pandas','requests','pathlib','azure.storage.blob'],
    author_email="fernando.colque@terranovatrading.com.pe",
)