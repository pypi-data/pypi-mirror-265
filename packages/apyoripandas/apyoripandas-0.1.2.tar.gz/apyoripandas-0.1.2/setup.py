from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="apyoripandas",
    version="0.1.2",
    description="Make easy user Apyori for Pandas",
    author="Matheus de Sá",
    author_email="matheusdesa55@gmail.com",
    url="https://github.com/matheus0sa/apyoripandas",
    packages=["apyoripandas"],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
     classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
