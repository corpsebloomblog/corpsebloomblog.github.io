import os
import glob

dir_path = os.path.dirname(os.path.realpath(__file__))


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


def fill_template():

    def scan_imports(contents):
        imports = []
        lines = contents.split("\n")
        for i in range(len(lines)):
            if '#insert ' in lines[i]:
                imports.append(lines[i][len("#insert "):])
        return imports
    
    def fetch_imports(imports):
        keys = dict()
        for asset in imports:
            keys[f"#insert {asset}"] = read_file(f"assets/{asset}")
        return keys
    
    def insert_imports(contents, import_key):
        for key in list(import_key.keys()):
            contents = [import_key[key] if line == key else line for line in to_lines(contents)]
        return from_lines(contents)

    files = glob.glob('template/**/*.html', recursive=True)
    for file in files:
        imports = scan_imports(read_file(file))
        keys = fetch_imports(imports)
        new_page = insert_imports(read_file(file), keys)
        new_destination = file.split("/")
        new_destination = new_destination[1:]
        new_destination = ["docs"] + new_destination
        os.makedirs("/".join(new_destination[:-1]), exist_ok = True)
        new_destination = "/".join(new_destination)

        write_file(new_destination, new_page)
    

fill_template()


