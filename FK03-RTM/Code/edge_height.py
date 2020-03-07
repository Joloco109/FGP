import matplotlib.pyplot as plt
import numpy as np
from reader import read_configure_graph
from fitting import lin_regression
from plot import plot_multifit, plot_fit
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

err = 7e-11
z_theo = [ 0,
        2.01e-9 ]

def edge_height( graph_name, config_name, file_name, draw_edge=False, print_paras=False ):
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

        if print_paras:
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
                "X"+graph.units[1], "Y"+graph.units[1], graph.name.replace("_"," "), directory="Graphs/"+file_name+"/", show=False)

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
        print("    ({:.2f} +- {:.2f})nm".format(row[0]*1e9, row[1]*1e9))

    return heights

def edge( edge ):
    height = []
    for i in range(1, len(edge_names[edge])+1):
        height += heights( edge, i )
    z = np.array([ x[0] for x in height ])
    z_err = np.array([ x[1] for x in height ])
    n = np.linspace(0,len(z),len(z))
    z_m = np.mean(z)
    z_m_err = np.std(z)
    plot_multifit( n, z, z_err, [n,n], [lambda x: np.ones(len(x))*z_m, lambda x: np.ones(len(x))*z_theo[edge]],
            "", "", "Z", show=True)

    print("z_theo = {:.3e}nm".format(z_theo[edge]*1e9))
    print("z = ({:.3e} +- {:.3e})nm".format(z_m*1e9, z_m_err*1e9))
    print("z-z_theo = {:.2f} sigma".format((z_m-z_theo[edge])/z_m_err))
