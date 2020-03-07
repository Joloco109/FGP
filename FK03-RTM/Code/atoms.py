import numpy as np
from reader import read_configure_tabular
from fitting import lineare_regression
from fitting import prop_regression
from plot import plot_fit
from plot import plot_multifit
import os

C = 246# pm
R_err = 40 #pm

data_dir = "Data/HOPG_Atoms/"
tab_names = [ "HOPG_Atoms_2_tab.txt",
        "HOPG_Atoms_2.5_tab.txt",
        "HOPG_Atoms_3_tab.txt",
        ]
conf_names = [ "HOPG_Atoms_2.conf",
        "HOPG_Atoms_2.5.conf",
        "HOPG_Atoms_3.conf",
        ]


def d( data, distance ):
    return distance * np.array([ np.sqrt( x[0]**2 + x[1]**2 - 2*x[0]*x[1]*np.cos(x[2]/360*2*np.pi) ) for x in data ])

def atoms( tab_name, config_name, title, offset=False):
    tab = read_configure_tabular( tab_name, config_name )
    dx_theo = d( tab[0].data, C )
    dy_theo = d( tab[1].data, C )

    dx = np.abs(np.array([ x[3] for x in tab[0].data ]))
    dy = np.abs(np.array([ x[4] for x in tab[1].data ]))

    if not os.path.exists("Graphs/HOPG_Atoms/"):
        os.makedirs("Graphs/HOPG_Atoms/")

    if not offset:
        x_fit = prop_regression( dx_theo, dx, R_err * np.ones(len(dx_theo)) )
        x_model = lambda x : x_fit[0] * x
    else:
        x_fit = lineare_regression( dx_theo, dx, R_err * np.ones(len(dx_theo)) )
        x_model = lambda x : x_fit[0] * x + x_fit[2]
    plot_fit( dx_theo, dx, R_err * np.ones(len(dx_theo)), x_model,
            "dxtheo", "dx", title+" X", directory="Graphs/HOPG_Atoms/", sort=True, show=True)

    if not offset:
        y_fit = prop_regression( dy_theo, dy, R_err * np.ones(len(dy_theo)) )
        y_model = lambda y : y_fit[0] * y
    else:
        y_fit = lineare_regression( dy_theo, dy, R_err * np.ones(len(dy_theo)) )
        y_model = lambda y : y_fit[0] * y + y_fit[2]
    plot_fit( dy_theo, dy, R_err * np.ones(len(dy_theo)), y_model,
            "dytheo", "dy", title+" Y", directory="Graphs/HOPG_Atoms/", sort=True, show=True)

    return ( x_fit, y_fit )

x_fit = []
y_fit = []
for (tab, conf) in zip( tab_names, conf_names ):
    x, y = atoms( (data_dir+"{}").format(tab), (data_dir+"{}").format(conf), conf[:-5].replace('_',' '))
    x_fit.append(x)
    y_fit.append(y)

print(    "a_y=")
for row in y_fit:
    print("    {:.4f} +- {:.4f}".format(row[0], row[1]))

print(    "a_x=")
for row in x_fit:
    print("    {:.4f} +- {:.4f}".format(row[0], row[1]))
