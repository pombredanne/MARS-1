from functions import *
import sys

""" 
def wrong_cuts(system):
    microservices = get_microservices(system)
    programming_languages = get_programming_languages()
    programming = 0
    notprogramming = 0
    for service in microservices:
        mainlang = get_main_lang(service)
        if mainlang.lower() in programming_languages:
            programming +=1
        elif mainlang.lower() == "Not-specified-language":
            notprogramming += 0
        else: 
            notprogramming += 1
    if notprogramming == 0 or programming == 0: return False
    return programming / notprogramming < 0.6

def circular_dependencies(system):
    call_graph = get_call_graph(system)
    return get_call_graph_cycles(call_graph)
"""
def mega_nano_service(system):
    
    # Values coming from the box plot
    NANO_SERVICE_THRESHOLD_NBFILES = 4
    NANO_SERVICE_THRESHOLD_LOCS = 95

    MEGA_SERVICE_THRESHOLD_NBFILES = 17
    MEGA_SERVICE_THRESHOLD_LOCS = 570

    megaservices = []
    nanoservices = []


    microservices = get_microservices(sys.argv[1])
    excluded_services = get_excluded_services(sys.argv[1])
    for microservice in microservices:
        ms_name = microservice.split("/")[-2]
        if ms_name not in excluded_services:
            cloc = os.popen("cloc " + microservice)
            output = cloc.read()
            if "-----" in output:
                lines = output.splitlines()
                for line in lines:
                    if line.lower().startswith("java"):
                        values = re.findall('\d+', line)  
            else:
                values = [1,1,1,1]
            
            if int(values[0]) < NANO_SERVICE_THRESHOLD_NBFILES and int(values[3]) < NANO_SERVICE_THRESHOLD_LOCS:
                nanoservices.append(ms_name)
            if int(values[0]) > MEGA_SERVICE_THRESHOLD_NBFILES and int(values[3]) > MEGA_SERVICE_THRESHOLD_LOCS:
                megaservices.append(ms_name)

    return megaservices, nanoservices
    
"""
def shared_libraries(system):
    shared_libs = []
    microservices = get_microservices(system)
    found_dependencies = []
    for service in microservices:
        service_dependencies = get_dependencies(system)
        for service_dependency in service_dependencies:
            if service_dependency.endswith(".jar"):
                if service_dependency in shared_libs:
                    return True
                else:
                    shared_libs.append(service_dependency)
    return False

def hardcoded_endpoints(system):
    system_dependencies = get_dependencies(system)
    source_files = get_source_files(system)
    config_files = get_config_files(system)
    compose_files = get_docker_compose_files(system)

    has_urls_in_source = check_urls_in_files(source_files)
    has_urls_in_conf = check_urls_in_files(config_files)   
    has_urls_in_compose = check_urls_in_files(compose_files)      

    return uses("service_discovery", system_dependencies) is False and (has_urls_in_conf or has_urls_in_source or has_urls_in_compose)


def manual_configuration(system):

    system_dependencies = get_dependencies(system)
    config_files = get_config_files(system)
    has_bootstrap_properties = has_bootstrap_props(config_files)
    has_cloud_in_app_config = app_properties_has_cloud_config(config_files)

    return uses("configuration", system_dependencies) is False and len(config_files) >= 1 and has_bootstrap_properties is False and has_cloud_in_app_config is False


def no_ci_cd(system):

    system_dependencies = get_dependencies(system)

    ci_folders_exists = has_ci_folders(system)
    ci_files_exists = has_ci_files(system)

    return (uses("cicd", system_dependencies) or ci_folders_exists or ci_files_exists) is False


def no_api_gateway(system):
    system_dependencies = get_dependencies(system)
    return uses("gateway", system_dependencies) is False


def timeouts(system):
    source_files = get_source_files(system)
    system_dependencies = get_dependencies(system)
    has_cb_annotation = check_cb_in_files(source_files)  

    return (uses("circuit_breaker", system_dependencies) or has_cb_annotation) is False


def msiph(system):
    compose_files = get_docker_compose_files(system)
    deploy_files = get_deploy_files(system)
    dockerfiles = get_docker_files(system)

    return len(deploy_files) >= 1 or len(compose_files) < 1 or len(dockerfiles) <= 1


def shared_persistence(system):
    source_files = get_source_files(system)
    compose_files = get_docker_compose_files(system)
    xml_files = get_xml_files(system)
    sql_files = get_sql_files(system)

    all_files = source_files + compose_files + xml_files + sql_files

    unique_datasource_urls = get_datasource_urls(all_files)
    unique_create_db_statements = get_create_db_statements(all_files)
    if len(unique_create_db_statements) == 0 and len(unique_datasource_urls) == 0:
        # No persistence layer
        return False
    else:
        return len(unique_create_db_statements) <= 1 and len(unique_datasource_urls) <= 1


def no_api_versioning(system):
    yaml_files = get_yaml_files(system)
    source_files = get_source_files(system)
    compose_files = get_docker_compose_files(system)

    has_versions_in_urls = are_versions_in_urls(source_files) and are_versions_in_urls(compose_files)
    has_api_version_key = api_version_key_exists(yaml_files)

    return (has_versions_in_urls or has_api_version_key) is False



def no_healthcheck(system):
    system_dependencies = get_dependencies(system)
    config_files = get_config_files(system)
    source_files = get_source_files(system)
    docker_files = get_docker_files(system)

    has_healthchecks_in_source = check_health_in_files(source_files)
    has_healthchecks_in_docker = check_health_in_dockerfiles(docker_files)
    enable_health_endpoints = check_health_is_enabled(config_files)


    return uses("healthcheck", system_dependencies) is False or (has_healthchecks_in_docker is False and has_healthchecks_in_source is False and enable_health_endpoints is False)

def local_logging(system):
    system_dependencies = get_dependencies(system)
    return uses("logging", system_dependencies) is False


def insufficient_monitoring(system):
    system_dependencies = get_dependencies(system)
    return uses("monitoring", system_dependencies) is False




print(sys.argv[1] + " Found AP WC : " + str(wrong_cuts(sys.argv[1])))
print(sys.argv[1] + " Found AP CD : " + str(circular_dependencies(sys.argv[1])))
"""
msns = mega_nano_service(sys.argv[1])
print(sys.argv[1] + " Found AP MS : " + str(msns[0]))
print(sys.argv[1] + " Found AP NS : " + str(msns[1]))
"""
print(sys.argv[1] + " Found AP SL : " + str(shared_libraries(sys.argv[1])))
print(sys.argv[1] + " Found AP HCE : " + str(hardcoded_endpoints(sys.argv[1])))
print(sys.argv[1] + " Found AP MC : " + str(manual_configuration(sys.argv[1])))
print(sys.argv[1] + " Found AP NCI : " + str(no_ci_cd(sys.argv[1])))
print(sys.argv[1] + " Found AP NAG : " + str(no_api_gateway(sys.argv[1])))
print(sys.argv[1] + " Found AP TO : " + str(timeouts(sys.argv[1])))
print(sys.argv[1] + " Found AP MSIPH : " + str(msiph(sys.argv[1]))) 
print(sys.argv[1] + " Found AP SP : " + str(shared_persistence(sys.argv[1])))
print(sys.argv[1] + " Found AP NAV : " + str(no_api_versioning(sys.argv[1])))
print(sys.argv[1] + " Found AP NHC : " + str(no_healthcheck(sys.argv[1])))
print(sys.argv[1] + " Found AP LL : " + str(local_logging(sys.argv[1])))
print(sys.argv[1] + " Found AP IM : " + str(insufficient_monitoring(sys.argv[1])))  """

