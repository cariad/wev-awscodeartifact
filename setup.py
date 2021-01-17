from pathlib import Path

from setuptools import setup

from wev_awscodeartifact.version import get_version

readme_path = Path(__file__).parent.joinpath("README.md")

with open(readme_path, encoding="utf-8") as f:
    long_description = f.read()

classifiers = [
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

version = get_version()

if "a" in version:
    classifiers.append("Development Status :: 3 - Alpha")
elif "b" in version:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")

classifiers.sort()

setup(
    author="Cariad Eccleston",
    author_email="cariad@hey.com",
    classifiers=classifiers,
    description='"wev" plugin for Amazon Web Services CodeArtifact authorisation',
    entry_points={
        "wev.plugins": "wev-awscodeartifact = wev_awscodeartifact",
    },
    include_package_data=True,
    install_requires=[
        "boto3>=1.16",
    ],
    license="MIT License",
    long_description=long_description,
    long_description_content_type="text/markdown",
    name="wev-awscodeartifact",
    packages=["wev_awscodeartifact"],
    python_requires=">=3.8",
    url="https://github.com/cariad/wev-awscodeartifact",
    version=version,
)
