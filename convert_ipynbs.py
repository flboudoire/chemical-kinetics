import os

files = [
    "examples/HMF_oxidation_WO3/HMF_oxidation_WO3",
    "examples/simple_example/simple_example"
    ]

for file in files:

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