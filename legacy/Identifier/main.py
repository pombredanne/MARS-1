import sys
import json
import math
import os
import re
from time import sleep
import pandas as pd
import networkx as nx

def scan_dependencies_global():
    deps = {}
    with open(sys.argv[1] + "/internal_dependencies.json") as dependencies:
        data = json.load(dependencies)
        for node in data:
            if(node["platform"] == "maven" and node["dependencies"]):
                if len(node["path"].split("/")) > 1:
                    microservice = node["path"].split("/")[1]
                    deps[microservice] = [item["name"] for item in node["dependencies"]]
        return deps


def get_microservices():
        microservices = []
        with open(sys.argv[1] + "/internal_dependencies.json") as dependencies:
            data = json.load(dependencies)
            for node in data:
                if len(node["path"].split("/")) > 1:
                    microservices.append(node["path"].split("/")[1])
        return microservices


def uses(needle):
    found = False
    found_libs = []
    with open('../tools/' + needle + ".txt") as f:
        lines = f.read().splitlines()
        # For each library used by the framework
        for lib in lines:
            for service in dependencies:
                if(lib in str(dependencies[service])):
                    found_libs.append(lib)
                    found = True
        return found, str(set(found_libs))

def count_dependencies(dependencies):
    dep_count = 0
    ms_count = 0
    for k,d in enumerate(dependencies):
        dep_count += len(d)
        ms_count += 1
    return dep_count, ms_count

def find_urls_in_code():
    with open(sys.argv[1] + "/files_list.json") as f:
        data = json.load(f)
        ms_urls = dict()
        if data["Java"]:
            for source_file in data["Java"]:
                ms_urls[source_file] = [x[0] for x in get_urls_in_file(sys.argv[1] + "/source/" + source_file)]
            # Search for docker compose files
            for root, directory, files in os.walk(sys.argv[1] + "/source/"):
                for filename in files:
                    if filename.endswith(".yml") or filename.endswith(".yaml"):
                        ms_urls[filename] = [x[0] for x in get_urls_in_file(os.path.join(root, filename))]
                        
        for filename in ms_urls:
            if len(ms_urls[filename]) > 0 :
                print(filename)
                print(ms_urls[filename])


def get_urls_in_file(source_file):
    urls = []
    if not "test" in str.lower(source_file):
        f = open(source_file)
        content = f.read()
        comment_regex = '//.*|("(?:\\[^"]|\\"|.)*?")|(?s)/\*.*?\*/'
        # content = re.sub(comment_regex, '', content)
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?????????????????]))"
        urls = re.findall(regex, content)
        f.close()
    return urls

def count_files_locs(directory):
    global_locs_cmd = os.popen("cloc " + sys.argv[1] + "/source/" + directory)
    global_locs = global_locs_cmd.read()
    temp_output = global_locs.split("SUM:")[1].split("\n")[0]
    integers = re.findall('\d+', temp_output)
    total_nb_files = integers[0]
    total_locs = integers[3]
    return total_nb_files, total_locs


def has_circular_dependencies():
    cycles = []
    found = False
    df = pd.read_csv(sys.argv[1] + "/callgraph.csv", delimiter=';', header=None)
    edges = [tuple(x) for x in df.values]
    G = nx.DiGraph(edges)

    for cycle in nx.simple_cycles(G):
        if(len(cycle) > 1):
            found = True
            cycles.append(cycle)
    return found, str(cycles)


microservices = get_microservices()
dependencies = scan_dependencies_global()
dependency_count = count_dependencies(dependencies)[0]
ms_count = count_dependencies(dependencies)[1]
avg_deps = math.ceil(dependency_count / ms_count)


find_urls_in_code()


print("Microservice Antipattern identification process starting...")
sleep(1)
print("Current microservice project : " + sys.argv[1])

print("\n")

print("GLOBAL ANTIPATTERNS")
print("*******************")

print("TIMEOUTS")
print("--------")
print("- Uses circuit breaker library : " + str(uses("circuit_breaker")[0]))
if(uses("circuit_breaker")):
    print("- Found library : " + uses("circuit_breaker")[1])
print("Identified AP : " + str(uses("circuit_breaker")[0] is False))

print("-----------------------------------------------------------------")

print("HARDCODED ENDPOINTS")
print("------------")
print("- Uses discovery library : " + str(uses("service_discovery")[0]))
print("- Has URLs in code : " + str("TBD"))
print("- Has URLs in config : " + str("TBD"))
if(uses("service_discovery")[0]):
    print("- Found library : " + uses("service_discovery")[1])
print("Identified AP : " + str(uses("service_discovery")[0] is False))

print("-----------------------------------------------------------------")

print("HEALTHCHECKS")
print("------------")
print("- Uses healthcheck library : " + str(uses("healthcheck")[0]))
print("- Uses docker healthchecks : " + str("TBD"))
if(uses("healthcheck")[0]):
    print("- Found library : " + uses("healthcheck")[1])
print("Identified AP : " + str(uses("healthcheck")[0] is False))

print("-----------------------------------------------------------------")

print("MANUAL CONFIGURATION")
print("--------------------")
print("- Uses configuration library : " + str(uses("configuration")[0]))
if(uses("configuration")[0]):
    print("- Found library : " + uses("configuration")[1])
print("Identified AP : " + str(uses("configuration")[0] is False))

print("-----------------------------------------------------------------")

print("CI/CD")
print("-----")
print("- Uses CI/CD library : " + str(uses("cicd")[0]))
print("- Uses CI/CD in repo : " + str("TBD"))
if(uses("cicd")[0]):
    print("- Found library : " + uses("cicd")[1])
print("Identified AP : " + str(uses("cicd")[0] is False))

print("-----------------------------------------------------------------")

print("API Gateway")
print("-----------")
print("- Uses Gateway library : " + str(uses("gateway")[0]))
print("- Clients calling services : " + str("TBD"))
if(uses("gateway")[0]):
    print("- Found library : " + uses("gateway")[1])
print("Identified AP : " + str(uses("gateway")[0] is False))

print("-----------------------------------------------------------------")


print("Circular Dependencies")
print("-----------")
print("- Has circular dependencies : " + str(has_circular_dependencies()[0]))
if(has_circular_dependencies()[0]):
    print("- Found circular dependencies : " + str(has_circular_dependencies()[1]))
print("Identified AP : " + str(has_circular_dependencies()[0] is True))

print("-----------------------------------------------------------------")

print("LOCAL LOGGING")
print("-------------")
print("- Uses logging libraries : " + str(uses("logging_monitoring")[0]))
if(uses("logging_monitoring")[0]):
    print("- Found library : " + uses("logging_monitoring")[1])
print("Identified AP : " + str(uses("logging_monitoring")[0] is False))

print("-----------------------------------------------------------------")

print("INSUFFICIENT MONITORING")
print("-----------------------")
print("- Uses monitoring libraries : " + str(uses("logging_monitoring")[0]))
if(uses("logging_monitoring")[0]):
    print("- Found library : " + uses("logging_monitoring")[1])
print("Identified AP : " + str(uses("logging_monitoring")[0] is False))






print("\n")
print("=============================================================================")
print("\n")
print("LOCAL ANTIPATTERNS")
print("******************")


total_files, total_locs = count_files_locs("")
system_avg_locs = math.ceil(int(total_locs) / int(ms_count))
system_avg_files = math.ceil(int(total_files) / int(ms_count))

print("Total services " + str(ms_count))
print("Total files " + str(total_files))
print("Total locs " + str(total_locs))
print("Total libraries " + str(dependency_count))
print("System avg files : " + str(system_avg_files))
print("System avg lines of code : " + str(system_avg_locs))
print("System avg libraries : " + str(avg_deps))

megaservices = []
nanoservices = []

for ms in microservices:
    if(ms in dependencies):
        if(os.path.isfile(sys.argv[1] + "/source/" + ms)):
            ms_nb_files = count_files_locs(ms)[0]
            ms_nb_locs = count_files_locs(ms)[1]
            ms_nb_deps = len(dependencies[ms])


            file_offset_percent = ((int(ms_nb_files) - int(system_avg_files)) / int(system_avg_files)) * 100
            loc_offset_percent = ((int(ms_nb_locs) - int(system_avg_locs)) / int(system_avg_locs)) * 100
            dep_offset_percent = ((int(ms_nb_deps) - int(avg_deps)) / int(avg_deps)) * 100


            is_mega = ((file_offset_percent + loc_offset_percent + dep_offset_percent) / 3) > 50
            is_nano = ((file_offset_percent + loc_offset_percent + dep_offset_percent) / 3) < -50

            print("\n\n")
            print(ms)
            print("================================")
            
            print("MEGA SERVICE / NANO SERVICE")
            print("------------")
            print("- Service files : " + str(ms_nb_files))
            print("- Service lines of code : " + str(ms_nb_locs))
            print("- Service libraries count : " + str(ms_nb_deps))
            
            print("- Nb files offset percentage : " + str(round(file_offset_percent,2)) + "%")
            print("- Nb LOCs offset percentage : " + str(round(loc_offset_percent,2)) + "%")
            print("- Nb libs offset percentage : " + str(round(dep_offset_percent,2)) + "%")

            print("Identified AP MEGA SERVICE : " + str(is_mega))
            print("Identified AP NANO SERVICE : " + str(is_nano))
            if(is_mega): 
                megaservices.append(ms)
            if(is_nano):
                nanoservices.append(ms)

print("\n\n\n")
print("----------------------------------------------------------")
print("IDENTIFICATION SUMMARY")
print("----------------------------------------------------------")
print("**************************************************************************************************")
print("TIMEOUTS ANTIPATTERN : " + str(uses("circuit_breaker")[0] is False))
print("HARDCODED ENDPOINTS ANTIPATTERN : " + str(uses("service_discovery")[0] is False))
print("NO HEALTHCHECK ANTIPATTERN : " + str(uses("healthcheck")[0] is False))
print("MANUAL CONFIGURATION ANTIPATTERN : " + str(uses("configuration")[0] is False))
print("NO CI/CD ANTIPATTERN : " + str(uses("cicd")[0] is False))
print("NO API GATEWAY ANTIPATTERN : " + str(uses("gateway")[0] is False))
print("LOCAL LOGGING : " + str(uses("logging_monitoring")[0] is False))
print("INSUFFICIENT MONITORING : " + str(uses("logging_monitoring")[0] is False))
print("MEGA SERVICES IDENTIFIED : ")
for s in megaservices:
    print("- " + s)
print("NANO SERVICES IDENTIFIED : ")
for s in nanoservices:
    print("- " + s)

print("**************************************************************************************************")
        
