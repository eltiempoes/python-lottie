Telegram Animated Stickers Tools
================================

A Python framework to work with Telegram animated stickers.


Scripts
-------

* `bin/lottieconvert.py`

  Script that can convert between several formats, including lottie / TGS

* `bin/tgs2lottie.py`

  Will extract a tgs file into a pretty printed JSON

* `bin/lottie2tgs.py`

  Will convert a lottie file into a tgs file

* `bin/svg2tgs.pt`

  Converts an SVG file into a lottie or tgs file

* `bin/lottiecat.py`

  Prints the given lottie file into a human-readable format

* `bin/lottiediff.py`

  Shows a side-by-side diff of the human-readable rendition of two lottie files

* `bin/lottie2svg.py`

  Extracts a frame as SVG from a lottie/tgs file

* `bin/raster2tgs.py`

  Converts a sequence of raster images into a lottie/tgs file


Installation
------------


### Synfig

There's a Synfig studio plugin to export telegram stickers.
To install, just copy (or symlink) ./synfig/tgs-exporter
into the synfig plugin directory.


Requirements
------------

Python 3.


### Optional Requirements

* `coverage` To show unit test coverage, used optionally by `test.sh`
* pillow, pypotrace>=0.2, numpy, scipy To convert raster images into vectors


Features
--------

Here is a list of features of the tgs python framework:

* Loading compressed TGS and uncompressed lottie JSON
* Importing SVG images
* Importing raster images and convert them into vectors
* Export lottie JSON or TGS
* Export (non-animated) SVG
* Export Synfig files
* Manipulation of lottie objects
* Simple animation presets (eg: shake, linear bounce)
* Bezier path animations (eg: follow path, making paths appear and disappear)
* Wave distortion animation (eg: for flags)
* Pseudo-3D rotations
* Animation easing functions
* Inverse Kinematic solver
* Pretty printing and comparison of lottie files


Reverse Engineering
-------------------

I had to reverse engineer the format because Telegram couldn't be bothered
providing the specs.

A TGS file is a gzip compressed JSON, the JSON data is described here:
https://mattia.basaglia.gitlab.io/tgs/group__Lottie.html#lottie_json

### Making your own exporters converters

#### Lottie format

If you can get the source image into lottie format, that's 90% of the work done.

I've ripped the format schema into Python classes in lib/tgs/objects/ which *should*
output the correct json. Eg:

    foo = tgs.Animation()
    # ...
    json.dump(foo.to_dict(), output_file)

#### TGS changes

Nothing major, just ensure the root JSON object has `tgs: 1`

#### Gzipping

The tgs file is the JSON described above compressed into a gzip,
and renamed to .tgs


License
-------

AGPLv3+ https://www.gnu.org/licenses/agpl-3.0.en.html


Credits
-------

Copyright 2019 (C) Mattia Basaglia


Documentation
-------------

https://mattia.basaglia.gitlab.io/tgs/index.html
