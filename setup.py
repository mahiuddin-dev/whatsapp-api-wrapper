from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="whatsapp_api",
    version="0.1.0",
    description="Python wrapper for the Meta WhatsApp API",
    author="Md Mahiuddin",
    author_email="dev.mahiuddin@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
)
