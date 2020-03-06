import numpy as np
import matplotlib.pyplot as plt

fontsize = 32

def plot_multifit(x, y, yerr, x_par, y_model_par, xname, yname, label, directory="", show=False):
    plt.rcParams.update({'font.size': fontsize})
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    
    data = np.array([x.tolist(), y.tolist(), yerr.tolist()]).T
    data.sort(0)
    data = data.T
    x,y,yerr = data

    for part, model_part in zip(x_par, y_model_par):
        part.sort()
        plt.plot(part, model_part(part), label=r'Fit', color='g', marker='', linewidth=4)
    plt.errorbar(x, y, yerr=yerr, marker='.',
            ecolor='r', capsize =  2, elinewidth=2, linewidth=0, label=r"Data")

    plt.title(label, fontsize=1.3*fontsize)
    plt.xlabel(xname, fontsize=fontsize)
    plt.ylabel(yname, fontsize=fontsize)

    if show:
        plt.show()

    plt.savefig(directory+label+'.eps')
    #plt.savefig(directory+label+'.eps', bbox_inches = "tight")

    plt.close()

def plot_fit(x, y, yerr, y_model, xname, yname, label, directory="", show=False):
    plot_multifit(x, y, yerr, [x], [y_model], xname, yname, label, directory=directory, show=show)

