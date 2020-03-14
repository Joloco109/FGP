from identifier import identify_file
from calibrate import calibrate
from calibrate import calibrate_file
from calibration import Calibration
from graph import Graph
from plot import plot_graph

from parameter import calibration_names
from parameter import calibration_lines

def calibrate_bayesian( am, plot_peaks=False, txt_output=False):
    cali = calibrate( am )

    energies = []
    energies_theo = []
    energies_res = []

    energies_seperate = []
    for i in range(len(calibration_names[ 1 if am else 0 ])):
        e, e_theo, e_res = identify_file( i, am, cali=cali,
                trans=calibration_lines[1 if am else 0][i],
                plot_peaks=plot_peaks, txt_output=txt_output )

        energies_seperate.append( (e, e_res) )
        e = [ (e1, e2, e3) for e1, e2, e3 in zip( e, e_theo, e_res) if not e2 == None ]
        e.sort(key=lambda x : x[0])
        e_res = [ (cali.getX( (x[0][0],x[2][0]) )[1], 0) for x in e ]
        e_theo = [ x[1] for x in e ]
        e = [ cali.getX(x[0])[:2] for x in e ]

        energies += e
        energies_theo += e_theo
        energies_res += e_res

    calibration = Graph( energies, energies_theo )

    fit = calibration.fit( "Bayesian Calibration", "pol1" )

    if txt_output:
        print(fit)
        print("C     = {:=8.3f} +- {:=8.3f}".format( fit.GetParameter(0), fit .GetParError(0) ))
        print("A     = {:=8.3f} +- {:=8.3f}".format( fit.GetParameter(1), fit.GetParError(1) ))
        print("Chi^2 = {:=7.2f}".format( fit.GetChisquare() ))
        print("Chi^2/NDF = {:=7.2f}".format( fit.GetChisquare()/fit.GetNDF() ))
        print()

    if plot_peaks:
        plot_graph( calibration, xName="Bins", save=True  )

    cali = Calibration( fit )
    return cali


def main():
    print("Am:")
    #calibrate_bayesian( True, plot_peaks=True, txt_output=True )
    print()
    print()

    print("Rö:")
    calibrate_bayesian( False, plot_peaks=True, txt_output=True )
    print()
    print()

if __name__ == "__main__":
    main()
