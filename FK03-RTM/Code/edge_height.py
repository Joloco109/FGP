import matplotlib.pyplot as plt
import numpy as np
from reader import read_configure_graph
from fitting import lin_regression
from plot import plot_multifit
import os

data_dir = "Data/HOPG_Edge/"

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

err = 2e-11

def edge_height( graph_name, config_name, file_name, draw_edge=False ):
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

        a = (pars_l[0] + pars_r[0])/2
        da = pars_l[0] - pars_r[0]
        b = (pars_l[1] + pars_r[1])/2
        db = pars_l[1] - pars_r[1]

        if draw_edge:
            x_middle = x_l[-1] + x_r[0]
            x_z = (np.linspace( -1, 1 )*db*a/(a**2+1)  + x_middle )/2
            z_x = lambda x : -1/a * x + b + (a + 1/a)*( x_middle )/2
            x_l = np.linspace( x_l[0], (-db*a/(a**2+1)  + x_middle)/2)
            x_r = np.linspace( (db*a/(a**2+1)  + x_middle)/2, x_r[-1])
        else:
            x_z = []
            z_x = lambda x: x

        if not os.path.exists("Graphs/"+file_name+"/"):
            os.makedirs("Graphs/"+file_name)
        plot_multifit( x, y, err*np.ones(len(x)), [x_l,x_r, x_z], [y_l_mod,y_r_mod, z_x],
                "X"+graph.units[1], "Y"+graph.units[1], graph.name.replace("_"," "), directory="Graphs/"+file_name+"/", show=True )

        x_l = graph_l.data[0][:-1]
        x_r = graph_r.data[0][0]
        x = (x_l+x_r)/2

        z = (pars_l[0]-pars_r[0])*x + pars_l[1]-pars_r[1]
        z_err = np.sqrt( x**2 *(cov_l[0][0]+cov_r[0][0])
                + cov_l[1][1] + cov_r[1][1]
                + 2*x*(cov_l[1][0] + cov_r[1][0])
                )

        z = np.sqrt( 1+a**2 ) * db
        z_err = np.sqrt( (db*da/2)**2 / (1+1/a**2)
                +(1+a**2) * ( cov_l[1][1] + cov_r[1][1] )
                )

        heights.append( (z, z_err) )
    print()
    return heights

def heights( edge, scale ):
    heights = edge_height( data_dir+edge_names[edge][scale-1], data_dir+config_names[edge][scale-1], config_names[edge][scale-1][:-5])
    print(    "z=")
    for row in heights:
        print("    ({:.4f} +- {:.4f})nm".format(row[0]*1e9, row[1]*1e9))
