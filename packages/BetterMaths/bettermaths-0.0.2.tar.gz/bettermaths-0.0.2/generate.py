import subprocess, sys, shutil

commandBase = "python"

try:
    import toml
except:
    #Install toml if not exist and reload file
    subprocess.run(["pip", "install", "toml"])
    subprocess.run([commandBase, __file__])
    sys.exit()

subprocess.run([commandBase, "-m", "build"])

try:
    subprocess.run(["pip", "uninstall", "BetterMaths", "-y"])
except:
    pass

with open("pyproject.toml", "r") as file:
    toml_data = toml.load(file)

version = toml_data["project"]["version"]

subprocess.run(["pip", "install", f"dist/bettermaths-{version}-py3-none-any.whl"])

# #Remove dist dir
# shutil.rmtree("dist")