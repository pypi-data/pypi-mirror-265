from setuptools import setup, find_packages

readme = open("./README.md", "r", encoding="utf-8")

setup(
    name="trujillo-azure-package",
    version="0.1.0",
    packages=find_packages(),
    license="MIT",
    long_description=readme.read(),
    long_description_content_type="text/markdown; charset=UTF-8",
    description="Paquete que tiene como proposito el brindar clases de permitan utilizar servicios de Microsoft Azure",
    author="Fernando Colque",
    install_requires=['azure.keyvault.secrets','azure.identity'],
    author_email="fernando.colque@terranovatrading.com.pe",
)