#!/usr/bin/env python3
import os
import setuptools
from functools import reduce
here = os.path.dirname(os.path.abspath(__file__))


# Works fine everywhere without `encoding` except on giltab CI *shrugs*
with open(os.path.join(here, "README.md"), "r", encoding='utf8') as fh:
    long_description = fh.read()


def find_packages(root="lottie"):
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


vfdir = os.path.dirname(os.path.abspath(__file__))
if not os.path.isfile(os.path.join(vfdir, ".version_full")):
    with open(os.path.join(vfdir, "version")) as vf:
        version = vf.read().strip() + "+src"
    with open(os.path.join(vfdir, ".version_full"), "w") as vf:
        vf.write(version)
else:
    with open(os.path.join(vfdir, ".version_full")) as vf:
        version = vf.read().strip()

extras_require = {
    "trace": ["pillow", "pypotrace>=0.2", "numpy", "scipy"],
    "images": ["pillow"],
    "PNG": ["cairosvg"],
    "GIF": ["cairosvg", "pillow"],
    "text": ["fonttools"],
    "video": ["opencv-python", "pillow", "numpy"],
    "emoji": ["grapheme"],
    "GUI": ["QScintilla"],
}
extras_require["all"] = list(reduce(lambda a, b: a | b, map(set, extras_require.values())))

setuptools.setup(
    name="lottie",
    version=version,
    author="Mattia Basaglia",
    author_email="mattia.basaglia@gmail.com",
    description="A framework to work with lottie files and telegram animated stickers (tgs)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mattia.basaglia/python-lottie/",
    package_dir={'': 'lib'},
    license="GNU Affero General Public License v3 or later (AGPLv3+)",
    packages=find_packages(),
    scripts=[
        os.path.join("bin", "raster_palette.py"),
        os.path.join("bin", "lottie_cat.py"),
        os.path.join("bin", "tgs_check.py"),
        os.path.join("bin", "lottie_convert.py"),
        os.path.join("bin", "lottie_diff.py"),
        os.path.join("bin", "lottie_fonts.py"),
        os.path.join("bin", "lottie_printcolor.py"),
        os.path.join("bin", "lottie_diagnostic.py"),
    ],
    keywords="telegram stickers tgs lottie svg animation",
    # https://pypi.org/classifiers/
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
    ],
    zip_safe=True,
    python_requires=">=3",
    extras_require=extras_require,
    test_suite="test",
    project_urls={
        "Code": "https://gitlab.com/mattia.basaglia/python-lottie/",
        "Documentation": "http://mattia.basaglia.gitlab.io/python-lottie/index.html",
        "Chat": "https://t.me/tgs_stuff",
        "Coverage": "http://mattia.basaglia.gitlab.io/python-lottie/coverage/",
        "Downloads": "http://mattia.basaglia.gitlab.io/python-lottie/downloads.html",
    },
    data_files=[(".", [".version_full"])],
)
