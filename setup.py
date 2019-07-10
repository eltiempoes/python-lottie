import setuptools
import os
here = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()


def find_packages(root="tgs"):
    absroot = os.path.join(here, "lib", root)
    paks = []
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
    version="0.1.0",
    author="Mattia Basaglia",
    author_email="mattia.basaglia@gmail.com",
    description="A framework to work with lottie / tgs files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mattia.basaglia/tgs/",
    package_dir={'': 'lib'},
    packages=find_packages(),
    scripts=[
        os.path.join("bin", "lottie2tgs.py"),
        os.path.join("bin", "lottiecat.py"),
        os.path.join("bin", "lottiediff.py"),
        os.path.join("bin", "svg2tgs.py"),
        os.path.join("bin", "tgs2lottie.py"),
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
)
