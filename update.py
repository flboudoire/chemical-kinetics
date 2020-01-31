import os
import re


# export jupyter notebook as markdown and format markdown output to center
# figures
ipynb_files = list()
for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".ipynb") and "checkpoint" not in file:
            name = file.replace(".ipynb", "")
            ipynb_files.append(os.path.join(root, name))

for file in ipynb_files:

    os.system(rf"jupyter nbconvert --to markdown {file}.ipynb")

    # center figures
    clean_md = ""
    with open(rf"{file}.md") as f:
        for line in f:
            if "![svg]" in line:
                line = line.replace("![svg](", "")
                line = line.replace(")", "")
                clean_md += rf"<p align='center'><img src = {line}></p>"
            else:
                clean_md += line

    with open(rf"{file}.md", "w") as f:
        f.write(clean_md)

    # clean math
    clean_md = ""
    with open(rf"{file}.md") as f:
        for line in f:
            if "$$" in line:
                pattern = r'\$\$(.*?)\$\$'
                repl = r".. math:: \1"
                clean_md +=  re.sub(pattern, repl, line)
            elif "$" in line:
                pattern = r'\$(.*?)\$'
                repl = r":math:`\1`"
                clean_md +=  re.sub(pattern, repl, line)
            elif "<table" in line:
                pattern = r'class\=\"(.*?)\"'
                repl = r"docutils"
                clean_md +=  re.sub(pattern, repl, line)
            else:
                clean_md += line

    fname = file.split("/")[-1]
    with open(rf"docs/notebooks/{fname}.md", "w") as f:
        f.write(clean_md)

# update documentation
os.system(r"cd docs; make clean; make html")

# copy images from examples
for file in ipynb_files:
    fname = file.split("/")[-1]
    os.system(rf"cp -ar {file}_files docs/_build/html/{fname}_files")

# git
os.system(r"git pull;git add .;git commit -a -m 'Auto update';git push;")