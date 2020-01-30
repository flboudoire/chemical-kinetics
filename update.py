import os


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

# update documentation
os.system(r"cd docs; make clean; make markdown")

# git
os.system(r"git pull;git add .;git commit -a -m 'Update';git push;")