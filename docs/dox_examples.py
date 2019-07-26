import os
import sys
import shutil
import subprocess
import importlib
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "examples"
))

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
example_path = os.path.join(root, "examples")
doxpath = os.path.join(root, "docs", "dox", "examples")




if os.path.exists(doxpath):
    shutil.rmtree(doxpath)
os.makedirs(doxpath)

examples = [
    fname[:-3]
    for fname in sorted(os.listdir(example_path))
    if fname.endswith(".py")
]

for example in examples:
    print(example)
    subprocess.run(["python3", os.path.join(example_path, example + ".py")])
    with open("/tmp/%s.html" % example, "r") as f:
        html = f.read()

    headstart = html.find("#bodymovin")
    headend = html.find("</head>")
    bodystart = html.find("<div")
    bodyend = html.find("</body>")
    html_include = html[headstart:headend] + html[bodystart:bodyend]

    with open(os.path.join(doxpath, example + ".dox"), "w") as f:
        f.write("""
/*!
    \example {example}.py

    \htmlonly[block]
    <style>{html_include}
    \endhtmlonly

    {extra}
*/

""".format(example=example, html_include=html_include, extra=importlib.import_module(example).__doc__))
