from setuptools import setup


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="SQLAlchemy-serializer",
    version="1.4.8",
    description="Mixin for SQLAlchemy-models serialization without pain",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Y-Bro",
    url="https://github.com/n0nSmoker/SQLAlchemy-serializer",
    keywords=["sqlalchemy", "serialize", "to_dict", "JSON"],
    packages=["sqlalchemy_serializer", "sqlalchemy_serializer.lib"],
    install_requires=[
        "SQLAlchemy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
