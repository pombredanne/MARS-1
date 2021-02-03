import os
import sys
from shutil import copyfile, rmtree
from git import Repo
import json
import time
import glob

repo_url = sys.argv[1]
base_metamodel_file = "../blank_metamodel.json"
metamodel_file = "../metamodel.json"

print("Cloning " + repo_url + " into current analyser microservice folder...")
for root, dirs, files in os.walk('../CurrentMBS/Source'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        rmtree(os.path.join(root, d))

Repo.clone_from(sys.argv[1], "../CurrentMBS/Source")
print("Cloning done")

print("Building git repository info into Meta-model...")
if os.path.exists(metamodel_file):
    os.remove(metamodel_file)

copyfile(base_metamodel_file, metamodel_file)

mm_file = open(metamodel_file, "r")
mm = json.load(mm_file)
mm_file.close()

mm["isGitRepository"] = 1
mm["gitInfo"]["importedAt"] = time.time()
mm["gitInfo"]["repoURL"] = repo_url

mm_file = open(metamodel_file, "w")
json.dump(mm, mm_file)
mm_file.close()
print("Writing git info done.")



