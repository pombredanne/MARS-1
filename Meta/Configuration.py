import glob
import re
import os

from .Http import Http
from .Database import Database

class Configuration:

    def __init__(self, service):
        self.service_path = service
        self.config_files = []
        self.db_statements = []
        self.urls = []

        self.parse_config()


    def parse_config(self):
        self.get_config_files()
        for f in self.config_files:
            with open(f, "r") as sf:
                content = sf.read().splitlines()
                for line in content:
                    self.urls.extend(self.get_urls_in_line(line))
                    self.db_statements.extend(self.get_db_in_line(line))
                        

    def get_config_files(self):
        with open("../files_needles/config_files.txt", "r") as files:
            possibles = files.read().splitlines()
            for possible in possibles:
                filelist = glob.glob(self.service_path + "**/" + possible, recursive=True)
                for f in filelist:
                    self.config_files.append(f)


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