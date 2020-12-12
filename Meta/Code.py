import glob
import re
import os

from .Http import Http
from .Database import Database
from .Annotation import Annotation
from .Import import Import


class Code:
    def __init__(self, service):
        self.service_path = service
        self.source_files = []
        self.all_files = []
        self.db_statements = []
        self.imports = []
        self.urls = []
        self.annotations = []
        self.main_lang = self.get_main_lang()

        self.parse_code()


    def get_callgraph_cycles(self, callgraph):
        cycles = []
        for cycle in nx.simple_cycles(callgraph):
            if(len(cycle) > 1):
                cycles.append(cycle)
        return cycles


    def parse_code(self):
        self.get_source_files()
        for f in self.source_files:
            with open(f, "r") as sf:
                content = sf.read().splitlines()
                for line in content:
                    self.annotations.extend(self.get_annotations_in_line(line))
                    self.imports.extend(self.get_imports_in_line(line))
                    

    def get_source_files(self):
        with open("../files_needles/source_files.txt", "r") as files:
            possibles = files.read().splitlines()
            for possible in possibles:
                filelist = glob.glob(self.service_path + "**/" + possible, recursive=True)
                for f in filelist:
                    self.source_files.append(f)



    def get_urls_in_line(self, line):
        excluded = [line.strip() for line in open('../tools/tlds.txt')]
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = []
        matches = re.findall(regex, line)
        if matches is not None:
            for match in matches:
                if any(ele in match[0] for ele in excluded) is False:
                    urls.append(Http(match[0]))
        return urls


    def get_annotations_in_line(self, line):
        if(line.startswith("@")):
            annotation = Annotation(line)
            return [annotation]
        return []


    def get_imports_in_line(self, line):
        if(line.startswith("import ")):
            import_statement = Import(line)
            return [import_statement]
        return []

    def get_db_in_line(self, line):
        if line.lower().startswith("create database if not exists"):
            line = line.replace(";", " ")
            db_statement = Database(line, "create")
            return [db_statement]
        elif line.lower().startswith("create database"):
            line = line.replace(";", " ")
            db_statement = Database(line, "create")
            return [db_statement]
        return []


    def get_main_lang(self):
        enry = os.popen("../enry " + self.service_path)
        toplang = enry.read()
        if(toplang):
            return toplang.split("%")[1].split()[0].lower().strip()
        else: 
            return "Not-specified-language"

    def get_code_languages(self):
        return [line.strip() for line in open('../tools/languages.txt')]

    def is_one_type(self):
        return self.main_lang.lower() not in self.get_code_languages()