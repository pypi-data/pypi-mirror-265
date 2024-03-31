import json

from setuptools import find_packages, setup

manifest = json.load(open("pix/manifest.json", "r"))
with open("README.md", "r") as f:
    long_description = f.read()
setup(
    name=manifest["name"],
    version=manifest["version"],
    author=manifest["author"],
    description=manifest["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=manifest["url"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "manifest.json",
        ]
    },
    install_requires=["pillow", "pillow-avif-plugin", "pillow-heif"],
    entry_points={
        "console_scripts": [
            "pix = pix.main:main",
        ],
    },
    python_requires=">=3.9",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics :: Editors",
        "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
    ],
)
