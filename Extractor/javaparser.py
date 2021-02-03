import glob
import javalang
import re


def getsourcefiles(service_path):
    source_files = []
    with open("files_needles/source_files.txt", "r") as files:
        possibles = files.read().splitlines()
        for possible in possibles:
            fileslist = glob.glob(service_path + "/**/" + possible, recursive=True)
            for f in fileslist:
                if "test" not in f.lower():
                    source_files.append(f)
        return source_files


def parse(source_file):
    file = open(source_file, "r")
    content = file.read()
    tree = javalang.parse.parse(content)
    file.close()
    return tree


def getmethods(tree):
    method = []
    for path, node in tree.filter(javalang.tree.MethodDeclaration):
        method.append(node.name)
    return method


def getannotations(tree):
    annotations = []
    for path, node in tree.filter(javalang.tree.Annotation):
        annotations.append(node.name)
    return annotations


def getimports(tree):
    imports = []
    for path, node in tree.filter(javalang.tree.Import):
        imports.append(node.path)
    return imports


def gethttpdb(source):
    file = open(source, "r")
    content = file.read()
    file.close()
    urls = []
    db_statements = []

    ###################
    # HTTP Detection  #
    ###################

    excluded_tlds = [line.strip() for line in open('tools/tlds.txt')]
    httpregex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([" \
                r"^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "

    matches = re.findall(httpregex, content)
    if matches is not None:
        for match in matches:
            if any(ele in match[0] for ele in excluded_tlds) is False:
                urls.append(match[0])

    return urls
