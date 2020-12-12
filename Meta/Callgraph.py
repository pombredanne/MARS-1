import pandas as pd
import networkx as nx

class Callgraph:
    def __init__(self, path):
        self.callgraph_csv = path.split("source")[0] + "callgraph.csv"
        self.graph = self.csv_to_graph(self.callgraph_csv)
        self.cycles = self.get_callgraph_cycles()


    def csv_to_graph(self, csv_file):
        df = pd.read_csv(csv_file, delimiter=';', header=None)
        edges = [tuple(x) for x in df.values]
        graph = nx.DiGraph(edges)
        return graph


    def get_callgraph_cycles(self):
        cycles = []
        for cycle in nx.simple_cycles(self.graph):
            if(len(cycle) > 1):
                cycles.append(cycle)
        return cycles