from reader import Hist
from peakfinder import Peaks, peak_fit
from plot import plot_hist, plot_graph
from lit_values_reader import read_tabular, lit_file
from graph import Graph
from calibration import Calibration

from parameter import calibration_elements, calibration_peaks, data_dir, am_dir, roe_dir, leer_names, calibration_names, paras

def calibrate_file( file_number, am, ohne_leer=True, show_spectral_lines=False, plot_peaks=False, txt_output=False ):
    file_name = calibration_names[ 1 if am else 0 ][file_number]
    if txt_output:
        print(file_name[:-4])
    directory = data_dir + (am_dir if am else roe_dir)
    empty = Hist.read( directory + leer_names[ 1 if am else 0 ], "Leer", "Leer" )
    spectrum = Hist.read( directory + file_name,
            "Spectrum {}".format(file_name[:-4]),
            "Spectrum {}".format(file_name[:-4]))
    elems = calibration_elements[1 if am else 0][file_number]


    lit_tab = read_tabular(lit_file)
    spectral_lines = [ [ column[i] for _, column in lit_tab ] for i in range(len(lit_tab[0][1]))  if lit_tab[0][1][i] in elems ]
    if show_spectral_lines:
        for line in spectral_lines:
            print(line)

    energies_theo = []
    if len(elems) == 1:
        for transition in calibration_peaks[ 1 if am else 0 ][file_number]:
            if transition == None:
                energies_theo.append( None )
                continue
            line = [ x for x in spectral_lines if x[0] == elems[0] and x[2] == transition ][0]
            if line[5] != None:
                energies_theo.append( (float(line[5]), float(line[6])) )
            elif line[3] != None:
                energies_theo.append( (float(line[3]), float(line[4])) )
            else :
                energies_theo.append( None )


    if ohne_leer:
        spectrum = Hist( spectrum.hist - empty.hist, "Spectrum", "Spectrum" )

    acc, height, fac, _ = paras[ 1 if am else 0 ][file_number]
    peaks = peak_fit( spectrum, accuracy=acc, peak_height=height, peak_fac=fac, plot_peaks=plot_peaks, txt_output=txt_output )
    if txt_output:
        print()

    energies = []
    energy_res = []

    for peak in peaks:
        if txt_output:
            print(peak)
            print("C     = {:=8.3f} +- {:=8.3f}".format( peak.GetParameter(0), peak.GetParError(0) ))
        for j in range(0, int((peak.GetNpar()-1)/3) ):
            energies.append( (peak.GetParameter(3*j+2), peak.GetParError(3*j+2)) )
            energy_res.append( (peak.GetParameter(3*j+3), peak.GetParError(3*j+3)) )
            if txt_output:
                print("A_{}   = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+1), peak.GetParError(3*j+1) ))
                print("mu_{}  = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+2), peak.GetParError(3*j+2) ))
                print("sig_{} = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+3), peak.GetParError(3*j+3) ))
        if txt_output:
            print("Chi^2 = {:=7.2f}".format( peak.GetChisquare() ))
            print("Chi^2/NDF = {:=7.2f}".format( peak.GetChisquare()/peak.GetNDF() ))
            print()

    if plot_peaks:
        plot_hist( spectrum, logy=False)

    return energies, energies_theo, energy_res

def calibrate( am, use_std=False, plot_peaks=False, txt_output=False ):
    energies = []
    energies_theo = []
    energies_res = []

    energies_seperate = []
    for i in range(len(calibration_names[ 1 if am else 0 ])):
        e, e_theo, e_res = calibrate_file( i, am, ohne_leer=True, plot_peaks=plot_peaks, txt_output=txt_output )
        energies_seperate.append( (e, e_res) )
        e = [ (e1, e2, e3) for e1, e2, e3 in zip( e, e_theo, e_res) if not e2 == None ]
        e.sort(key=lambda x : x[0])
        e_res = [ x[2] for x in e ]
        e_theo = [ x[1] for x in e ]
        e = [ x[0] for x in e ]

        energies += e
        energies_theo += e_theo
        energies_res += e_res
    if use_std:
        calibration = Graph(
                [ (e[0], e_std[0]) for e, e_std in zip(energies, energies_res) ]
                , energies_theo )
    else:
        calibration = Graph( energies, energies_theo )
    fit = calibration.fit( "Calibration", "pol1" )
    if txt_output:
        print(fit)
        print("C     = {:=9.4f} +- {:=9.4f}".format( fit.GetParameter(0), fit .GetParError(0) ))
        print("A     = {:=9.4f} +- {:=9.4f}".format( fit.GetParameter(1), fit.GetParError(1) ))
        print("Chi^2 = {:=7.2f}".format( fit.GetChisquare() ))
        print("Chi^2/NDF = {:=7.2f}".format( fit.GetChisquare()/fit.GetNDF() ))
        print()
    if plot_peaks:
        plot_graph( calibration, xName="Bins", save=True  )

    cali = Calibration( fit )
    return cali


def main():
    print("Am:")
    calibrate( True, plot_peaks=True, txt_output=True )
    print()
    print()

    print("Rö:")
    calibrate( False, plot_peaks=True, txt_output=True  )
    print()
    print()

if __name__ == "__main__":
    main()
