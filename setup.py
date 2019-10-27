#!/usr/bin/env python3
import setuptools
import os
here = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()


def find_packages(root="tgs"):
    absroot = os.path.join(here, "lib", root)
    paks = [root]
    for sub in os.listdir(absroot):
        if sub == "__pycache__":
            continue
        lname = os.path.join(root, sub)
        if os.path.isdir(os.path.join(absroot, sub)):
            paks += [lname]
            paks += find_packages(lname)
    return paks


setuptools.setup(
    name="tgs",
    version=os.environ.get("VERSION_OVERRIDE", "0.3.5"),
    author="Mattia Basaglia",
    author_email="mattia.basaglia@gmail.com",
    description="A framework to work with lottie / tgs files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mattia.basaglia/tgs/",
    package_dir={'': 'lib'},
    packages=find_packages(),
    scripts=[
        os.path.join("bin", "raster2tgs.py"),
        os.path.join("bin", "raster_palette.py"),
        os.path.join("bin", "tgs2svg.py"),
        os.path.join("bin", "tgscat.py"),
        os.path.join("bin", "tgsconvert.py"),
        os.path.join("bin", "tgsdiff.py"),
        os.path.join("bin", "tgsfonts.py"),
        os.path.join("bin", "tgsprintcolor.py"),
    ],
    keywords="telegram stickers tgs lottie svg animation",
    # https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
    ],
    zip_safe=True,
    python_requires=">=3",
    extras_require={
        "Vectorization": ["pillow", "pypotrace>=0.2", "numpy", "scipy"],
        "Load image": ["pillow"],
        "PNG": ["cairosvg"],
        "Text": ["fonttools"],
    },
    test_suite="test",
    project_urls={
        "Code": "https://gitlab.com/mattia.basaglia/tgs/",
        "Documentation": "https://mattia.basaglia.gitlab.io/tgs/index.html",
        "Chat": "https://t.me/tgs_stuff",
        "Coverage": "https://mattia.basaglia.gitlab.io/tgs/coverage/",
    },
)
