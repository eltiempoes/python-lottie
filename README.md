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
To install, just copy (or symlink) ./addons/synfig/tgs-exporter
into the synfig plugin directory.

(Note: the bulk of this code has nothing to do with this package)

### Inkscape

There are some import/export extensions for inkscape.

Just copy (or symlink) the files under ./addons/inkscape to the inkscape extension
directory.
On my system that's ~/.config/inkscape/extensions/ but you can double check from
Inkscape: Edit > Preferences... > System > User extensions

Note that the extensions require Python 3.
If they are run with a python 2 interpreter, they will try to run themselves using `python3`.

They also need the tgs framework to be in the python path, otherwise you can manually
set the path on the import/export dialogues.

See also https://inkscape.org/~mattia.basaglia/%E2%98%85tgslottie-importexport


### Blender

There are some export addons for blender.

Copy (or symlink) the files under ./addons/blender to the Blender extension
directory.

On my system that's ~/.config/blender/2.80/scripts/addons/ you can check available
paths through the Blender Python console:

    import addon_utils; print(addon_utils.paths())

You can also install the addon from Blender using the zipfile created by `make`.


Requirements
------------

Python 3.


### Optional Requirements

* `coverage`                            To show unit test coverage, used optionally by `test.sh`
* `pillow`, `pypotrace>=0.2`, `numpy`, `scipy` To convert raster images into vectors
* `pillow`                              To load image assets
* `cairosvg`                            To export PNG / PDF / PS
* `cairosvg`, `pillow`                  To export GIF
* `cairosvg`, `numpy`, Python OpenCV 2  To export video
* `fonttools`                           To render text as shapes


Features
--------

Here is a list of features of the tgs python framework:

* Loading compressed TGS and uncompressed lottie JSON
* Importing SVG images
* Importing raster images and convert them into vectors
* Export lottie JSON or TGS
* Export (non-animated) SVG
* Export Synfig files
* Export PNG/PDF/PostScript
* Export GIF
* Export Video (MP4, AVI, WebM)
* Manipulation of lottie objects
* Simple animation presets (eg: shake, linear bounce)
* Bezier path animations (eg: follow path, making paths appear and disappear)
* Wave distortion animation (eg: for flags)
* Pseudo-3D rotations
* Animation easing functions
* Inverse Kinematic solver
* Pretty printing and comparison of lottie files
* Rendering text as shapes


Reverse Engineering
-------------------

I had to reverse engineer the format because Telegram couldn't be bothered
providing the specs.

A TGS file is a gzip compressed JSON, the JSON data is described here:
https://mattia.basaglia.gitlab.io/tgs/group__Lottie.html#lottie_json

### Making your own exporters converters

#### Lottie format

If you can get the source image into lottie format, that's 90% of the work done.

I've created Python classes based the format schema and after effects documentation, which
output the correct json. Eg:

    foo = tgs.Animation()
    # ...
    json.dump(foo.to_dict(), output_file)

I'm also creating a proper documentation for the format, see:
https://mattia.basaglia.gitlab.io/tgs/group__Lottie.html#details

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
* Solids


The following things are actually unsupported:

* Layer Effects
* Images
* Skew transforms (this isn't listed in the unsupported features)
* Texts
* Animated layer transforms (not listed as unsupported)


Things marked as unsupported that I haven't tested:

* Expressions
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
