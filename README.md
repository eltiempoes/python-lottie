Telegram Animated Stickers Tools
================================

A Python framework to work with Telegram animated stickers.


Scripts
-------

* `bin/tgsconvert.py`

  Script that can convert between several formats, including lottie / TGS

* `bin/tgscat.py`

  Prints the given tgs / lottie file into a human-readable format

* `bin/tgsdiff.py`

  Shows a side-by-side diff of the human-readable rendition of two tgs / lottie files

* `bin/tgs2svg.py`

  Extracts a frame as SVG from a lottie/tgs file, has a couple more options than `bin/tgsconvert.py`

* `bin/raster2tgs.py`

  Converts a sequence of raster images into a lottie/tgs file, has a couple more options than `bin/tgsconvert.py`

* `bin/raster_palette.py`

  Shows the palette of a raster image, to use with `bin/raster2tgs.py`

* `bin/tgscolor.py`

  Converts a CSS color into a normalized array, as used in lottie

* `bin/jsoncat.py`

  Pretty prints a JSON file (useful to debug / diff lottie files)

* `bin/jsondiff.py`

  Pretty prints two JSON files side by side, highlighting differences (useful to debug / diff lottie files)

* `bin/tgscat.py`

  Pretty prints a tgs / lottie file with more readable annotations (useful to debug / diff lottie files)

* `bin/tgsdiff.py`

  Pretty prints two tgs / lottie files side by side, highlighting differences (useful to debug / diff lottie files)


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
* pillow to load image assets


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


#### Unsupported features

Telegram doesn't support everything in the Lottie format.
https://core.telegram.org/animated_stickers lists some things that are unsupported
but what is listed there isn't correct.

There are several things marked as unsupported in telegram animated stickers that are actually supported:

* Masks
* Mattes (Works on desktop but not on Android)
* Star Shapes
* Gradient Strokes
* Repeaters


The following things are actually unsupported:

* Layer Effects
* Images
* Skew transforms (this isn't listed in the unsupported features)


Things marked as unsupported that I haven't tested:

* Expressions
* Solids
* Texts
* 3D Layers
* Merge Paths
* Time Stretching
* Time Remapping
* Auto-Oriented Layers


License
-------

AGPLv3+ https://www.gnu.org/licenses/agpl-3.0.en.html


Credits
-------

Copyright 2019 (C) Mattia Basaglia


Links
-----

### Documentation

https://mattia.basaglia.gitlab.io/tgs/index.html

### Code

https://gitlab.com/mattia.basaglia/tgs/

### Chat

https://t.me/tgs_stuff
