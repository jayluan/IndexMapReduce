import networkx as nx
import numpy as np
import re

class Utility:


    def __init__(self):
        self.pages = nx.Graph()

    def addNodes(self, urls):
        self.pages.add_nodes_from(urls)

    def addEdges(self, relationships):
        for entry in relationships:
            for edge in entry:
                self.pages.add_edge(edge[0], edge[1])
