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
                clean_md += rf"<p align='center'>{line}</p>"
            else:
                clean_md += line

    with open(rf"{file}_clean.md", "w") as f:
        f.write(clean_md)