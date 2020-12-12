import os
import glob
import json
import networkx as nx

from .Microservice import Microservice
from .Dependency import Dependency
from .Callgraph import Callgraph

class System:
    def __init__(self, path):
        self.project_root = path
        self.dependencies = self.get_dependencies()
        self.microservices = self.get_microservices()
        self.callgraph = self.get_callgraph()


    def get_microservices(self):

        microservices = []

        rootpath = self.project_root.split("source")[0]
        exclude_file = open(rootpath + "exclude.txt", "r")
        excluded_services = exclude_file.read().split()

        all_services = glob.glob(self.project_root + "*/")
        
        for service in all_services:
            ms_name = service.split("/")[-2]
            if ms_name not in excluded_services:
                microservice = Microservice(service)
                microservices.append(microservice)

        return microservices

    def get_dependencies(self):
        dependencies = []
        os.system('ruby ../ManifestParser/scanner.rb ' + self.project_root + ' > ../temp/raw_dependencies.json')
        with open("../temp/raw_dependencies.json") as raw_dependencies:
            data = json.load(raw_dependencies)
            for node in data:
                if(node["platform"] == "maven" and node["dependencies"]):
                    for item in node["dependencies"]:
                        dep = Dependency(item)
                        dependencies.append(dep)
        return dependencies    

    def get_callgraph(self):
        callgraph = Callgraph(self.project_root)
        return callgraph



