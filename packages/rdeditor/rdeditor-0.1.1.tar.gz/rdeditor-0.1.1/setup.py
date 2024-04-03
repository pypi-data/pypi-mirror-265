from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="rdeditor",
    version="0.1.1",
    description="An RDKit based molecule editor using PySide",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="RDKit molecule editor pyside",
    url="http://github.com/ebjerrum/rdeditor",
    author="Esben Jannik Bjerrum",
    author_email="esbenjannik@rocketmail.com",
    license="LGPL",
    packages=["rdeditor"],
    package_data={"rdeditor": ["pixmaps/*"]},
    install_requires=["PySide2", "numpy", "rdkit"],
    python_requires=">=3.8, <3.11",
    entry_points={
        "console_scripts": [
            "rdEditor = rdeditor.rdEditor:launch",
        ],
    },
    extras_require={"dev": ["ruff"]},
    zip_safe=False,
)
