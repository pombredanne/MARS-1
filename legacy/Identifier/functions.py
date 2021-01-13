import sys
import os
import json
import glob
import re 
import pandas as pd
import networkx as nx


def get_files(filetype, system):
    matches = []
    with open("../files_needles/" + filetype + ".txt", "r") as files:
        possibles = files.read().splitlines()
        for possible in possibles:
            filelist = glob.glob(system + "**/" + possible, recursive=True)
            for f in filelist:
                matches.append(f)
    return matches

def get_dependencies(system):
    dependencies = []
    os.system('ruby ../ManifestParser/scanner.rb ' + system + ' > temp/raw_dependencies.json')
    with open("temp/raw_dependencies.json") as raw_dependencies:
        data = json.load(raw_dependencies)
        for node in data:
            if(node["platform"] == "maven" and node["dependencies"]):
                for item in node["dependencies"]:
                    dependencies.append(item["name"])
    return dependencies    


def get_config_files(system):
    return get_files("config_files", system)

def get_source_files(system):
    return get_files("source_files", system)

def get_docker_files(system):
    return get_files("docker_files", system)

def get_docker_compose_files(system):
    return get_files("docker_compose", system)

def get_yaml_files(system):
    return get_files("yaml_files", system)

def get_xml_files(system):
    return get_files("xml_files", system)

def get_sql_files(system):
    return get_files("sql_files", system)

def get_deploy_files(system):
    return get_files("deploy_files", system)

def check_health_in_files(source_files):
    for source in source_files:
        with open(source, "r") as sf:
            content = sf.read()
            comment_regex = '//.*|("(?:\\[^"]|\\"|.)*?")|(?s)/\*.*?\*/'
            content = re.sub(comment_regex, '', content)
            content.splitlines()
            for line in content:
                if "health" in line:
                    return True
    return False


def check_health_in_dockerfiles(docker_files):
    for source in docker_files:
        with open(source, "r") as sf:
            content = sf.read().splitlines()
            for line in content:
                if "HEALTHCHECK" in line:
                    return True
    return False


def check_health_is_enabled(configuration_files):
    for configuration_file in configuration_files:
        if configuration_file.endswith(".properties"):
            with open(configuration_file, "r") as cf:
                content = cf.read().splitlines()
                for line in content:
                    if "management.endpoint.health.enabled=true" in line or "management.endpoints.web.exposure.include=*" in line:
                        return True
    return False

def has_bootstrap_props(configuration_files):
    return "bootstrap.properties" in configuration_files


def app_properties_has_cloud_config(configuration_files):
    for configuration_file in configuration_files:
        if configuration_file.endswith("application.properties"):
            with open(configuration_file, "r") as cf:
                content = cf.read().splitlines()
                for line in content:
                    if "spring.cloud.config" in line:
                        return True
    return False


def has_ci_folders(system):
    with open("../files_needles/ci_folders.txt", "r") as cif:
        content = cif.read().splitlines()
        for line in content:
            if os.path.isdir(system + line):
                return True
    return False

def has_ci_files(system):
    return len(get_files("ci_files", system)) > 0


def get_urls_in_content(content):
    excluded = [line.strip() for line in open('../tools/tlds.txt')]
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    urls = []
    for line in content:
        matches = re.findall(regex, line)
        if matches is not None:
            for match in matches:
                if any(ele in match[0] for ele in excluded) is False:
                    urls.append(match[0])
    return urls

def check_urls_in_files(source_files):
    urls = []
    for source in source_files:
        with open(source, "r") as sf:
            content = sf.read().splitlines()
            found = get_urls_in_content(content)
            urls.extend(found)
    return len(urls) > 1


def get_urls_in_files(source_files):
    urls = []
    for source in source_files:
        with open(source, "r") as sf:
            content = sf.read().splitlines()
            found = get_urls_in_content(content)
            urls.extend(found)
    return urls
    
    
def check_cb_in_files(source_files):
    for source in source_files:
        with open(source, "r") as sf:
            content = sf.read().splitlines()
            for line in content:
                if "@EnableCircuitBreaker" in line or ("@HystrixCommand" in line and "fallbackMethod" in line) or "CircuitBreakerFactory" in line:
                    return True
    return False


def api_version_key_exists(yaml_files):
    for yaml_file in yaml_files:
        with open(yaml_file, "r") as yf:
            content = yf.read().splitlines()
            for line in content:
                if "apiVersion" in line:
                    return True
    return False

def are_versions_in_urls(files):
    urls = get_urls_in_files(files)
    if urls is not None:
        for url in urls:
            version_found = re.findall('/version\d+', url)
            v_found = re.findall('/v\d+', url)
            if version_found or v_found:
                return True
    return False


def get_datasource_urls(files):
    ds_urls = []
    for u_file in files:
        with open(u_file, "r") as f:
            content = f.read().splitlines()
            for line in content:
                if "mysql://" in line:
                    line = line.replace('"', " ").replace("'", " ").replace(",", " ")
                    ds_urls.append(line.split("mysql://")[1].split()[0])
    return list(set(ds_urls))

def get_create_db_statements(files):
    cdb_statements = []
    for u_file in files:
        with open(u_file, "r") as f:
            content = f.read().splitlines()
            for line in content:
                if "create database if not exists" in line.lower():
                    line = line.replace(";", " ")
                    print(line)
                    cdb_statements.append(line.lower().split("exists")[1].split()[0])
                elif "create database" in line.lower():
                    line = line.replace(";", " ")
                    print(line)
                    cdb_statements.append(line.lower().split("create database")[1].split()[0])
    return list(set(cdb_statements))


def get_microservices(system):
    return glob.glob(system + "*/")


def cloc(directory):
    cloc = os.popen("cloc " + directory)
    output = cloc.read()
    if "-----" in output:
        sum_line = output.splitlines()[-2]
        values = re.findall('\d+', sum_line)
    else:
        values = [1,1,1,1]
    return values


def get_call_graph(system):
    rootpath = sys.argv[1].split("source")[0]
    df = pd.read_csv(rootpath + "callgraph.csv", delimiter=';', header=None)
    edges = [tuple(x) for x in df.values]
    graph = nx.DiGraph(edges)

    return graph


def get_excluded_services(system):
    rootpath = sys.argv[1].split("source")[0]
    exclude_file = open(rootpath + "exclude.txt", "r")
    excluded_services = exclude_file.read().split()
    return excluded_services
    

def get_call_graph_cycles(callgraph):
    cycles = []
    for cycle in nx.simple_cycles(callgraph):
        if(len(cycle) > 1):
            cycles.append(cycle)
    return cycles


def get_main_lang(system):
    enry = os.popen("../enry " + system)
    toplang = enry.read()
    if(toplang):
        return toplang.split("%")[1].split()[0].lower().strip()
    else: 
        return "Not-specified-language"


def get_programming_languages():
    return [line.strip() for line in open('../tools/languages.txt')]

def uses(category, dependencies):
    with open("../tools/" + category + ".txt", "r") as tools:
        list_of_tools = tools.read().splitlines()
        for lib in list_of_tools:
            for dep in dependencies:
                if(lib in str(dep)):
                    return True
    return False