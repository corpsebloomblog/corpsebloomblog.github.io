import os
import glob

POSTS_FOLDER = "posts"
TARGET_FOLDER = "docs"

TITLE = "#TITLE"
SUBTITLE = "#SUBTITLE"
ALTTITLE = "#ALTTITLE"
TEMPLATE = "#TEMPLATE"
PATH = "#PATH"
DATE = "#DATE"
SERIES = "#SERIES"

TEXT_KEY = "[text]"
TITLE_KEY = "[title]"
SUBTITLE_KEY = "[subtitle]"
DATE_KEY = "[date]"


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


files = glob.glob(f"template/**/*.meta", recursive=True)
for file in files:
    lines = to_lines(read_file(file))

    keys = [
        TITLE, 
        SUBTITLE,
        ALTTITLE,
        TEMPLATE,
        PATH,
        DATE,
        SERIES,
    ]

    metadata = dict()

    for line in lines:
        for key in keys:
            if f"{key}: " in line: metadata[key] = line[len(f"{key}: "):]

    template_location = str(f"{TARGET_FOLDER}/{metadata[PATH]}/template.html")
    
    # insert text into page
    new_page = read_file(template_location).replace(TEXT_KEY, read_file(file.split(".")[0]+".html"))
    
    # insert other data values into page
    new_page = new_page.replace(TITLE_KEY, metadata[TITLE])
    new_page = new_page.replace(SUBTITLE_KEY, metadata[SUBTITLE])
    new_page = new_page.replace(DATE_KEY, metadata[DATE])

    # write to file
    new_destination = file.split(".")[0]+".html"
    new_destination = new_destination.split("/")[-1]
    os.makedirs(f"docs/{metadata[PATH]}", exist_ok = True)
    new_destination = f"docs/{metadata[PATH]}/{new_destination}"

    write_file(new_destination, new_page)