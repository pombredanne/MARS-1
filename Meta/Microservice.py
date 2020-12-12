import os
import re
import json
from .Dependency import Dependency
from .Code import Code
from .Configuration import Configuration

class Microservice:

    def __init__(self, service):
        self.path = service
        self.name = self.path.split("/")[-2]
        self.loc_nb_files = self.get_locs()
        self.dependencies = self.get_dependencies()
        self.nb_files = self.loc_nb_files[0]
        self.locs = self.loc_nb_files[3]
        self.code = Code(service)
        self.config = Configuration(service)



    def get_locs(self):
        cloc = os.popen("cloc " + self.path)
        output = cloc.read()
        values = [1,1,1,1]
        if "-----" in output:
            lines = output.splitlines()
            for line in lines:
                if line.lower().startswith("java"):
                    values = re.findall('\d+', line)  
            
        return values


    def get_dependencies(self):
        dependencies = []
        os.system('ruby ../ManifestParser/scanner.rb ' + self.path + ' > ../temp/raw_dependencies.json')
        with open("../temp/raw_dependencies.json") as raw_dependencies:
            data = json.load(raw_dependencies)
            for node in data:
                if(node["platform"] == "maven" and node["dependencies"]):
                    for item in node["dependencies"]:
                        dep = Dependency(item)
                        dependencies.append(dep)
        return dependencies    

    
