from setuptools import setup, find_packages

setup(
    name="bmpi",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "argparse"
    ],
    entry_points={
        "console_scripts": [
            "bmpi = bmpi.main:main"
        ]
    }
)
