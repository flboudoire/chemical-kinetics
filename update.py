import os
import re
import sys
import shutil

version = "1.0"

def list_notebooks():
    """ find all notebooks in current directory and subdirectories
    """

    ipynb_files = list()
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb") and "checkpoint" not in file:
                name = file.replace(".ipynb", "")
                ipynb_files.append(os.path.join(root, name))

    return ipynb_files


def export_notebooks(ipynb_files):
    """ export jupyter notebook as markdown and format markdown output
    to center figures
    """

    ipynb_files = list()
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".ipynb") and "checkpoint" not in file:
                name = file.replace(".ipynb", "")
                ipynb_files.append(os.path.join(root, name))

    for file in ipynb_files:

        os.system(rf"jupyter nbconvert --to rst {file}.ipynb")

        # center figures and set table style
        clean_file = ""
        with open(rf"{file}.rst") as f:
            for line in f:
                line = line.replace(".. code:: ipython3", ".. code:: python3")
                if ".. image::" in line:
                    clean_file += line
                    clean_file += "  :align: center"
                elif "<table" in line:
                    pattern = r'class\=\"(.*?)\"'
                    repl = r"class = 'docutils'"
                    clean_file +=  re.sub(pattern, repl, line)
                elif any(s in line for s in [":mod:", ":func:", ":class:", ":meth:"]):
                    clean_file += line.replace("``", "`")
                else:
                    clean_file += line


        with open(rf"{file}.rst", "w") as f:
            f.write(clean_file)

        # move rst files and assets
        fname = file.split("/")[-1]
        os.system(rf"mv {file}.rst docs/source/{fname}.rst")
        os.system(rf"rm -r docs/source/{fname}_files")
        os.system(rf"mv {file}_files docs/source/{fname}_files")


if __name__ == "__main__":

    # pip
    if len(sys.argv) < 2 or sys.argv[1] == "pip":
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        dmy = os.popen(r"grep 'version=\".*\"' setup.py").read()
        v = int(dmy.split(".")[-1].split("\"")[0])
        version += f".{v+1}"
        os.system(fr"sed -i s/version=\".*\"/version=\"{version}\"/g setup.py")
        os.system(fr"sed -i s/version=\".*\"/version=\"{version}\"/g docs/source/conf.py")
        os.system(
            r"python3 setup.py sdist bdist_wheel;twine upload dist/* --skip-existing")

    # docs
    if len(sys.argv) < 2 or sys.argv[1] == "docs":
        # get all jupyter notebook paths
        ipynb_files = list_notebooks()

        # export jupyter notebooks examples
        export_notebooks(ipynb_files)

        # update documentation
        os.system(r"cd docs; make clean; make html")

    # git
    if len(sys.argv) < 2 or sys.argv[1] == "git":
        os.system(r"git pull;git add .;git commit -a -m 'Auto update';git push;")
