import os
import glob
import shutil


INSERT_PREFIX = "#insert "
TEMPLATE_FOLDER = "docs"
IMPORTS_FOLDER = "fragments"
TARGET_FOLDER = "docs"


def read_file(file):
    with open(file, 'r') as f:
        return f.read()

def write_file(file, string):
    with open(file, 'w+') as f:
        f.write(string)

def to_lines(string):
    return string.split("\n")

def from_lines(split):
    if type(split) == list:
        return "\n".join(split)
    if type(split) == str:
        return split


def scan_imports(contents):
    imports = []
    lines = contents.split("\n")
    for i in range(len(lines)):
        if INSERT_PREFIX in lines[i]:
            imports.append(lines[i][len(INSERT_PREFIX):])
    return imports

def fetch_imports(imports):
    keys = dict()
    for asset in imports:
        keys[f"{INSERT_PREFIX}{asset}"] = read_file(f"{IMPORTS_FOLDER}/{asset}")
    return keys

def insert_imports(contents, import_key):
    for key in list(import_key.keys()):
        contents = [import_key[key] if line == key else line for line in to_lines(contents)]
    return from_lines(contents)

files = glob.glob(f'{TEMPLATE_FOLDER}/**/*.html', recursive=True)
shutil.copytree(TEMPLATE_FOLDER, TARGET_FOLDER, dirs_exist_ok=True)

for file in files:
    imports = scan_imports(read_file(file))
    keys = fetch_imports(imports)
    new_page = insert_imports(read_file(file), keys)
    
    new_destination = file.split("/")
    new_destination = new_destination[1:]
    new_destination = [TARGET_FOLDER] + new_destination
    os.makedirs("/".join(new_destination[:-1]), exist_ok = True)
    new_destination = "/".join(new_destination)

    write_file(new_destination, new_page)


