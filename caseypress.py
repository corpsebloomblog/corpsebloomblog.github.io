import glob
from datetime import datetime
from sys import argv


CONFIG = "config"

# PAGE METADATA PARSING
META_TEMPLATE = "TEMPLATE"
META_TITLE = "TITLE"
META_SUBTITLE = "SUBTITLE"
META_DATE = "DATE"
META_SERIES = "SERIES"
# INDEX METADATA / CONFIG
META_TARGET_FOLDER = "TARGET"
META_POSTS_FOLDER = "POSTS"
META_POST_TEMPLATE = "LINK TEMPLATE"
META_INDEX_TEMPLATE = "INDEX TEMPLATE"
META_INDEX_NAME = "INDEX NAME"
# METADATA OTHER
SEPARATOR = ": "

# PAGE TEMPLATING
TEMPLATE_TITLE = "[TITLE]"
TEMPLATE_SUBTITLE = "[SUBTITLE]"
TEMPLATE_DATE = "[DATE]"
TEMPLATE_TEXT = "[TEXT]"
# INDEX TEMPLATING
TEMPLATE_KEY_POSTS = "[BLOGPOSTS]"
TEMPLATE_LINK = "[LINK]"
# TEMPLATING OTHER
NO_SERIES = "none"

POST_EXTENSION = "html"
META_EXTENSION = "meta"

#--
# HELPER FUNCTIONS
#--

def read_file(file):
    with open(file, 'r') as f:
        return f.read()


def write_file(file, string):
    with open(file, 'w+') as f:
        f.write(string)


def parse_metadata(string):
    string = string.split("\n")
    metadata = dict()
    for line in string:
        line = line.split(SEPARATOR)
        metadata[line[0]] = line[1]
    return metadata


def fill_template(text, keypairs):
    for keypair in keypairs:
        text = text.replace(keypair[0], keypair[1])
    return text

def sort_by_latest(post_metadata_pairs):
	post_metadata_pairs.sort(key=lambda x: datetime.strptime(x[1][META_DATE], "%d/%m/%Y"), reverse = True)
	return post_metadata_pairs


#--
# SCRIPT
#--

if len(argv) == 2:
	CONFIG = argv[1]




config = parse_metadata(read_file(CONFIG))

posts = glob.glob(f"{config[META_POSTS_FOLDER]}/**/*.{POST_EXTENSION}", recursive = True)
metadata = glob.glob(f"{config[META_POSTS_FOLDER]}/**/*.{META_EXTENSION}", recursive = True)

post_metadata_pairs = []
for post in posts:
	meta = (post[:-len(POST_EXTENSION)]+META_EXTENSION)
	if meta in metadata:
		post_metadata_pairs.append((post, meta))
	else:
		print(f"WARNING: .meta FILE FOR {post} MISSING")

parsed = []
for pair in post_metadata_pairs:
	post = read_file(pair[0])
	meta = parse_metadata(read_file(pair[1]))
	filename = pair[0].split("/")[-1]
	parsed.append((post, meta, filename))
parsed = sort_by_latest(parsed)


index = read_file(config[META_INDEX_TEMPLATE])
for post in parsed:
	template = read_file(config[META_POST_TEMPLATE])
	meta = post[1]
	keypairs = [
		(TEMPLATE_TITLE, meta[META_TITLE]),
		(TEMPLATE_DATE, meta[META_DATE]),
		(TEMPLATE_SUBTITLE, meta[META_SUBTITLE]),
		(TEMPLATE_LINK, post[2][:-(len(POST_EXTENSION)+1)])
	]
	post_text = fill_template(template, keypairs)

	index = index.replace(TEMPLATE_KEY_POSTS, post_text+"\n"+TEMPLATE_KEY_POSTS)
index = index.replace(TEMPLATE_KEY_POSTS, "")
write_file(f"{config[META_TARGET_FOLDER]}/{config[META_INDEX_NAME]}", index)


for parsed_post in parsed:
	post = parsed_post[0]
	meta = parsed_post[1]
	filename = parsed_post[2]

	template = read_file(meta[META_TEMPLATE])
	keypairs = [
		(TEMPLATE_TITLE, meta[META_TITLE]), 
		(TEMPLATE_SUBTITLE, meta[META_SUBTITLE]),
		(TEMPLATE_DATE, meta[META_DATE]),
		(TEMPLATE_TEXT, post)
	]
	filled_post = fill_template(template, keypairs)
	
	write_file(f"{config[META_TARGET_FOLDER]}/{filename}", filled_post)