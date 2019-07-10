Telegram Animated Stickers Tools
================================


Scripts
-------

* bin/tgs2lottie.py Will extract a tgs file into a pretty printed JSON
* bin/lottie2tgs.py Will convert a lottie file into a tgs file
* bin/svg2tgs.pt    Converts an SVG file into a lottie or tgs file
* bin/lottiecat.py  Prints the given lottie file into a human-readable format
* bin/lottiediff.py SHows a side-by-side diff of the human-readable rendition of two lottie files


Installation
------------


### Synfig

There's a Synfig studio plugin to export telegram stickers.
To install, just copy (or symlink) ./synfig/tgs-exporter
into the synfig plugin directory.


Requirements
------------

Python 3.


Reverse Engineering
-------------------

I had to reverse engineer the format because Telegram couldn't be bothered
providing the specs.

Seems a gzip compressed json, with a modified version of this format:
https://github.com/airbnb/lottie-web/tree/master/docs/json


### Making your own exporters converters

#### Lottie format

If you can get the source image into lottie format, that's 90% of the work done.

I've ripped the format schema into Python classes in lib/tgs.py which *should*
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
