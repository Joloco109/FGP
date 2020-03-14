from identifier import identify_file
from recalibrate import calibrate_bayesian
from graph import Graph
from plot import plot_graph
from parameter import file_names, calibration_lines

def energy_res( am, plot_peaks=False, txt_output=False):
    cali = calibrate_bayesian( am )

    energies = []
    energies_res = []

    for i in range(len(file_names[ 1 if am else 0 ])):
        e, _, e_res = identify_file( i, am, cali=cali,
                trans=calibration_lines[1 if am else 0][i],
                plot_peaks=plot_peaks, txt_output=txt_output )

        e = [ (e1, e2) for e1, e2 in zip( e, e_res) if not e2 == None ]
        e.sort(key=lambda x : x[0])
        if i == 6:
            del e[2]
        e_res = [ x[1] for x in e ]
        e = [ x[0] for x in e ]

        energies += e
        energies_res += e_res

    for e, e_res in zip(energies,energies_res):
        print(e, e_res)

    calibration = Graph( energies, energies_res )

    fit = calibration.fit( "Energy Resolution", "[0]*sqrt(x)" )

    if txt_output:
        print(fit)
        print("C     = {:=8.3f} +- {:=8.3f}".format( fit.GetParameter(0), fit .GetParError(0) ))
        print("Chi^2 = {:=7.2f}".format( fit.GetChisquare() ))
        print("Chi^2/NDF = {:=7.2f}".format( fit.GetChisquare()/fit.GetNDF() ))
        print()

    if plot_peaks:
        plot_graph( calibration )
