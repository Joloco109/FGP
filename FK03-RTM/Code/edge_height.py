import matplotlib.pyplot as plt
import numpy as np
from reader import read_configure_graph
from fitting import lin_regression
from plot import plot_multifit
import os

data_dir = "Data/"

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

config_names = [
        [ "HOPG_Edge2_100.conf",
            "HOPG_Edge2_200.conf",
            "HOPG_Edge2_300.conf"
            ],
        [ "HOPG_Edge_100.conf",
            "HOPG_Edge_200.conf",
            "HOPG_Edge_300.conf"
            ],
    ]

err = 1e-11

def edge_height( graph_name, config_name, file_name ):
    graphs = read_configure_graph( graph_name, config_name )
    heights = []
    for graph, graph_l, graph_r in graphs:
        x = np.array([ x[0] for x in graph.data ])
        y = np.array([ x[1] for x in graph.data ])

        x_l = np.array([ x[0] for x in graph_l.data ])
        y_l = np.array([ x[1] for x in graph_l.data ])
        pars_l, cov_l = lin_regression( x_l, y_l, err*np.ones(len(x_l)) )
        y_l_mod = lambda x : pars_l[0]*x+pars_l[1]

        x_r = np.array([ x[0] for x in graph_r.data ])
        y_r = np.array([ x[1] for x in graph_r.data ])
        pars_r, cov_r = lin_regression( x_r, y_r, err*np.ones(len(x_r)) )
        y_r_mod = lambda x : pars_r[0]*x+pars_r[1]

        print(graph.name)
        print("Paras:")
        print("L:\t({:.4e} +- {:.4e})".format(pars_l[0], cov_l[0][0] ))
        print("R:\t({:.4e} +- {:.4e})".format(pars_r[0], cov_r[0][0] ))
        print()

        if not os.path.exists("Graphs/"+file_name+"/"):
            os.makedirs("Graphs/"+file_name)
        plot_multifit( x, y, err*np.ones(len(x)), [x_l,x_r], [y_l_mod,y_r_mod],
                "X"+graph.units[1], "Y"+graph.units[1], graph.name.replace("_"," "), directory="Graphs/"+file_name+"/", show=True )

        x_l = graph_l.data[0][:-1]
        x_r = graph_r.data[0][0]
        x = (x_l+x_r)/2
        z = (pars_l[0]-pars_r[0])*x + pars_l[1]-pars_r[1]
        z_err = np.sqrt( x**2 *(cov_l[0][0]+cov_r[0][0])
                + cov_l[1][1] + cov_r[1][1]
                + 2*x*(cov_l[1][0] + cov_r[1][0])
                )
        heights.append( (z, z_err) )
    return heights

#edge_height( edge_names[0][0], config_names[0][0] )
