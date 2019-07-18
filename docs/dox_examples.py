import os
import shutil
import subprocess

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
    \page example_{example} {example}.py

    \htmlonly[block]
    <style>{html_include}
    \endhtmlonly

    \include {example}.py
*/

""".format(example=example, html_include=html_include))

with open(os.path.join(doxpath, "examples.dox"), "w") as f:
    f.write("""
/**
    \page examples Examples

{list}
*/
""".format(
    list="\n".join(
        "- \subpage example_{example}".format(example=example)
        for example in examples
    )
))
