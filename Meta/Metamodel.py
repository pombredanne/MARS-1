from .Code import Code
from .System import System


class Metamodel:
    def __init__(self, project_path):
        self.project_path = project_path
        self.system = System(self.project_path)
        self.microservices = self.system.get_microservices()
        self.dependencies = self.system.get_dependencies()
        self.callgraph = self.system.get_callgraph()
        





        