import networkx as nx
import numpy as np
import re

class Utility:


    def __init__(self):
        self.pages = nx.DiGraph()

    def addNodes(self, urls):
        self.pages.add_nodes_from(urls)

    def pageRank(self):
    	return nx.pagerank(self.pages)

    def addEdges(self, relationships):
        for entry in relationships:
            for edge in entry:
                self.pages.add_edge(edge[0], edge[1])
