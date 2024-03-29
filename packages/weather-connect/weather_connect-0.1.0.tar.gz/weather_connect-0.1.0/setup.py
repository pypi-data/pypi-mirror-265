import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "weather_connect",
    version = "0.1.0",
    author = "Faclon-Labs",
    author_email = "reachus@faclon.com",
    description = "weather connect library",
    packages = ["weather_connect"],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires=[
        'pymongo',
        'pandas',
        'requests',
        'datetime'
],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)