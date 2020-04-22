#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name="tgs",
    version="0.6.0",
    author="Mattia Basaglia",
    author_email="mattia.basaglia@gmail.com",
    description="A framework to work with lottie / tgs files",
    long_description="This project as moved to https://pypi.org/project/lottie/",
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/lottie/",
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    keywords="telegram stickers tgs lottie svg animation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
    ],
    zip_safe=True,
    requires=[
        "lottie"
    ],
    python_requires=">=3",
)
