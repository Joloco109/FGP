import numpy as np
import re

from reader import Hist
from calibrate import calibrate
from lit_values_reader import read_tabular, lit_file
from bayesian_inf import ModelDist
from peakfinder import Peaks, peak_fit
from plot import plot_hist, plot_graph

from parameter import elements, data_dir, am_dir, roe_dir, leer_names, file_names, paras


def spectral_line( elems=None, trans=None ):
    lit_tab = read_tabular(lit_file)
    lit_tab = [ [ column[i] for _, column in lit_tab ] for i in range(len(lit_tab[0][1])) if not lit_tab[0][1][i]==None ]
    if not elems == None:
        lit_tab = [ row for row in lit_tab if row[0] in elems  ]
    if not trans == None:
        if isinstance( trans[0], tuple ) :
            lit_tab = sum([ [ row for row in lit_tab if (row[0] == e and row[2] in t) ] for e,t in trans ], [])
        else:
            lit_tab = [ row for row in lit_tab if bool([ '' for t in trans if bool(re.match(t, row[2])) ]) ]
    lit_tab = [ (
        x[0], None if x[1]==None else int(x[1]), x[2],
        None if x[3]==None else float(x[3]), None if x[3]==None else float(x[4]),
        None if x[5]==None else float(x[5]), None if x[5]==None else float(x[6]),
        None if x[7]==None else float(x[7]), None if x[7]==None else float(x[8]),
        None if x[9]==None else float(x[9]), None if x[9]==None else float(x[10]),
        x[11]
        ) for x in lit_tab ]
    return lit_tab

def identify_peak( peak, lines ):
    energies = [ ((l[0],l[2]), [
        ((None
        if l[6]==None else (l[6], l[8]))
        if l[5]==None else (l[5], l[6]))
        if l[3]==None else (l[3], l[4])
        ]) for l in lines if not (l[6]==None and l[4]==None and l[2]==None) ]

    model = ModelDist( energies )
    model.Update( (peak[0], np.sqrt(peak[1]**2+peak[2]**2)) )
    return model.Result(), (model.Mean(), np.sqrt(model.Var()))

def identify_element( peaks, elems=None, trans=None ):
    lines = spectral_line( elems=elems, trans=trans )
    names = list(set([ l[0] for l in lines ]))
    energies = [ [
        ((None
        if l[6]==None else (l[6], l[8]))
        if l[5]==None else (l[5], l[6]))
        if l[3]==None else (l[3], l[4])
        for l in lines if not (l[6]==None and l[4]==None and l[2]==None) and l[0] == element ]
        for element in names ]

    model = ModelDist(list(zip( names, energies )))
    for peak in peaks:
        model.Update( (peak[0], np.sqrt(peak[1]**2+peak[2]**2)) )
    return model.Result()


def identify_file( file_number, am, ohne_leer=True, plot_peaks=False, txt_output=False ):
    elems = elements[1 if am else 0][file_number]
    lines_K = spectral_line( elems=elems, trans="K" )
    lines_L = spectral_line( elems=elems, trans="L" )

    cali = calibrate( am )

    file_name = file_names[ 1 if am else 0 ][file_number]
    if txt_output:
        print(file_name[:-4])
    directory = data_dir + (am_dir if am else roe_dir)

    empty = Hist.read( directory + leer_names[ 1 if am else 0 ],
            "Leer",
            "Leer",
            calibration=cali )

    spectrum = Hist.read( directory + file_name,
            "Spectrum {}".format(file_name[:-4]),
            "Spectrum {}".format(file_name[:-4]),
            calibration=cali)

    if ohne_leer:
        spectrum = Hist( spectrum.hist - empty.hist, "Spectrum", "Spectrum" )

    acc, height, fac, max_candidates = paras[ 1 if am else 0 ][ file_number ]
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

    means = []
    for e, sig_e in zip( energies, energy_res ):
        try :
            peak = identify_peak( (e[0], sig_e[0], 0), lines_K )
            candidates = peak[0][:max_candidates]
            means.append(peak[1])
        except ValueError:
            candidates = []
        try :
            peak = identify_peak( (e[0], sig_e[0], 0), lines_L )
            candidates += peak[0][:max_candidates//2]
            means.append(peak[1])
        except ValueError:
            candidates += []

        if txt_output:
            print("Peak: ({} +- {}) keV candidates:".format( e[0], sig_e[0] ))
            for c in candidates:
                print("\t",c)
            print()
            for m, sig in means:
                print("E = ({:.3f} +- {:.3f})keV".format( m/1e3, sig/1e3))

    if plot_peaks:
        plot_hist( spectrum, logy=False)
