import matplotlib.pyplot as plt
import numpy as np
from reader import read_configure_graph
from scipy.optimize import curve_fit

edge_names = [
        [ "HOPG_Edge2_100_Graph.txt",
            "HOPG_Edge2_200_Graph.txt",
            "HOPG_Edge2_300_Graph.txt"
            ],
        [ "HOPG_Edge_100_Graph.txt",
            "HOPG_Edge_200_Graph.txt",
            "HOPG_Edge_300_Graph.txt"
            ],
    ]

config1_names = [
        [ "HOPG_Edge2_100_Graph.txt",
            "HOPG_Edge2_200_Graph.txt",
            "HOPG_Edge2_300_Graph.txt"
            ],
        [ "HOPG_Edge_100_Graph.txt",
            "HOPG_Edge_200_Graph.txt",
            "HOPG_Edge_300_Graph.txt"
            ],
    ]

def edge_height( graph_name, config_name ):
    graphs = read_configure_graph( graph_name, config_name )
    for graph, graph_l, graph_r in graphs:
        graph



#edge_height( edge_names[0][0], config_names[0][0] )
