from setuptools import setup, find_packages

setup(
    name="whatsapp_api_wrapper",
    version="0.1.0",
    description="Python wrapper for the Meta WhatsApp API",
    author="Md Mahiuddin",
    author_email="dev.mahiuddin@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.32.3"
    ],
)
