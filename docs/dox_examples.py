import os
import sys
import shutil
import inspect
import importlib
import subprocess
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "examples"
))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "lib"
))
from lottie.objects.animation import Animation
from lottie.exporters.core import HtmlOutput

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
example_path = os.path.join(root, "examples")
doxpath = os.path.join(root, "docs", "dox", "examples")

if len(sys.argv) > 1:
    examples = sys.argv[1:]
else:
    examples = [
        fname[:-3]
        for fname in sorted(os.listdir(example_path))
        if fname.endswith(".py")
    ]

    if os.path.exists(doxpath):
        shutil.rmtree(doxpath)

os.makedirs(doxpath, exist_ok=True)

for example in examples:
    example_fn = os.path.join(example_path, example + ".py")
    module = importlib.import_module(example)

    with open(os.path.join(doxpath, example + ".dox"), "w") as f:
        f.write("""/*!
\example {example}.py

\htmlonly[block]
""".format(example=example))

        for obj in vars(module).values():
            if isinstance(obj, Animation):
                out = HtmlOutput(obj, f)
                out.style()
                out.body_pre()
                out.body_embedded()
                out.body_post()
                break

        f.write("\\endhtmlonly\n\n")
        f.write(inspect.getdoc(module) or "")
        f.write("\n\n*/\n\n")
