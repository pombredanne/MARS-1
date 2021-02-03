import inquirer
import os
import json
import dependencies
import microservices
import javaparser
import dockerfiles

mbsroot = "../CurrentMBS/Source"
folders = [f.name for f in os.scandir(mbsroot) if f.is_dir()]
metamodel_file = "../metamodel.json"
'''
questions = [
    inquirer.Checkbox('exclude',
                      message="Please select folders that are not actual microservices in the directory structure",
                      choices=folders,
                      ),
]
excludes = inquirer.prompt(questions)
print("Thank you, excluding folders from analysis...")
with open("../CurrentMBS/exclude.txt", "w") as outfile:
    outfile.write("\n".join(excludes["exclude"]))
'''
print("Folders excluded, building meta-model...")

mm_file = open(metamodel_file, "r")
mm = json.load(mm_file)
mm_file.close()

##################################
# Extracting system dependencies #
##################################
'''
print("Extracting system wide dependencies")
system_deps = dependencies.extract(mbsroot)
print("Dependencies extracted, writing to meta-model")
mm["system"]["dependencies"] = system_deps
mm_file = open(metamodel_file, "w")
json.dump(mm, mm_file)
mm_file.close()
print("Writing done")
'''
##################################
# Extracting microservices       #
##################################

print("Extracting microservices")
system_ms = microservices.extract(mbsroot)
ms_node = []
print("microservices extracted, reading information")
for microservice in system_ms:
    ms_data = {}
    service_path = mbsroot + "/" + microservice
    cloc_out = microservices.getlocs(service_path)
    ms_data["name"] = microservice
    ms_data["language"] = microservices.getlang(service_path)
    ms_data["nb_files"] = cloc_out[0]  # The first returned value
    ms_data["locs"] = cloc_out[3]  # The third returned value
    ms_data["dependencies"] = dependencies.extract(service_path)
    ms_data["code"] = dict()
    ms_data["code"]["imports"] = []
    ms_data["code"]["annotations"] = []
    ms_data["code"]["methods"] = []
    ms_data["code"]["http"] = []
    ms_data["code"]["databases"] = []
    ms_data["code"]["source_files"] = javaparser.getsourcefiles(service_path)
    ms_data["deployment"] = dict()
    ms_data["deployment"]["docker_files"] = dockerfiles.getdockerfiles(service_path)
    ms_data["deployment"]["images"] = []
    # For every source file in this microservice
    for source in ms_data["code"]["source_files"]:
        # Build his AST tree
        tree = javaparser.parse(source)
        ms_data["code"]["annotations"] += javaparser.getannotations(tree)
        ms_data["code"]["methods"] += javaparser.getmethods(tree)
        ms_data["code"]["imports"] += javaparser.getimports(tree)

        # Removing potential duplicates
        ms_data["code"]["annotations"] = list(dict.fromkeys(ms_data["code"]["annotations"]))
        ms_data["code"]["methods"] = list(dict.fromkeys(ms_data["code"]["methods"]))
        ms_data["code"]["imports"] = list(dict.fromkeys(ms_data["code"]["imports"]))

        httpdb = javaparser.gethttpdb(source)

        ms_data["code"]["http"] += httpdb

    for dockerfile in ms_data["deployment"]["docker_files"]:
        parsed_dockerfile = dockerfiles.parse(dockerfile)
        ms_data["deployment"]["images"].append(parsed_dockerfile.baseimage)

    ms_node.append(ms_data)


print("Writing microservices info into meta-model")

mm_file = open(metamodel_file, "r")
mm = json.load(mm_file)
mm_file.close()

mm["system"]["microservices"] = ms_node

mm_file = open(metamodel_file, "w")
json.dump(mm, mm_file)
mm_file.close()
print("Writing done")
