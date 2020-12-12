import sys
sys.path.append('../')

from Meta.Metamodel import Metamodel

metamodel = Metamodel(sys.argv[1])

print("System path : " + metamodel.system.project_root)
print("Callgraph cycles: " + str(metamodel.system.callgraph.cycles))
print("System dependencies : ")
for dep in metamodel.system.dependencies:
    print(dep.name)
print("\n")
print("System microservices : ")
for ms in metamodel.system.microservices:
    print(ms.name + " : ")
    print("\tLOCS : " + str(ms.locs))
    print("\tNB Files : " + str(ms.nb_files))
    print("URLS in code: " + str(ms.code.urls))
    print("Imports : " + str(ms.code.imports))
    print("Annotations : " + str(ms.code.annotations))
    print("DBs in code : " + str(ms.code.db_statements))
    print("URLs in config : " + str(ms.config.urls))
    print("DBs in config : " + str(ms.config.db_statements))
    