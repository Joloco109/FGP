from reader import Hist
from peakfinder import Peaks, peak_fit
from plot import plot_hist
from lit_values_reader import read_tabular, lit_file

data_dir = "Data/"
am_dir = "Am/"
roe_dir = "Röhre/"

leer_names = [
        "Leer.mca",
        "Leer.mca"
        ]

calibration_names = [ [
            "Kupfer.mca",
            "Silber.mca",
            "Stahl.mca"
        ],[
            "Copper.mca",
            "Silber.mca",
            "Stahl.mca",
            "Barium.mca",
            "Molybden.mca",
            "Rubidium.mca",
            "Terbium.mca"
        ]
    ]

calibration_elements = [ [
            [ "Cu" ],
            [ "Ag" ],
            [ "Fe", "Mo", "Cr", "Ni" ]
        ],[
            [ "Cu" ],
            [ "Ag" ],
            [ "Fe", "Mo", "Cr", "Ni" ],
            [ "Ba" ],
            [ "Mo" ],
            [ "Rb" ],
            [ "Tb" ]
        ]
    ]

paras = [ ( 5, 1.5e2, 5 ),
        ( 5, 5e1, 5 )]

def calibrate( file_number, am, ohne_leer=True ):
    directory = data_dir + (am_dir if am else roe_dir)
    empty = Hist.read( directory + leer_names[ 1 if am else 0 ], "Leer", "Leer" )
    spectrum = Hist.read( directory + calibration_names[ 1 if am else 0 ][file_number], "Spectrum", "Spectrum" )
    elems = calibration_elements[1 if am else 0][file_number]

    lit_tab = read_tabular(lit_file)
    spectral_lines = [ [ column[i] for _, column in lit_tab ] for i in range(len(lit_tab[0][1]))  if lit_tab[0][1][i] in elems ]
    for line in spectral_lines:
        print(line)

    if ohne_leer:
        spectrum = Hist( spectrum.hist - empty.hist, "Spectrum", "Spectrum" )

    acc, height, fac = paras[ 1 if am else 0 ]
    peaks = peak_fit( spectrum, accuracy=acc, peak_height=height, peak_fac=fac)

    energies = []
    energy_res = []

    for peak in peaks:
        print(peak)
        print("C     = {:=8.3f} +- {:=8.3f}".format( peak.GetParameter(0), peak.GetParError(0) ))
        for j in range(0, int((peak.GetNpar()-1)/3) ):
            energies.append( (peak.GetParameter(3*j+2), peak.GetParError(3*j+2)) )
            energy_res.append( (peak.GetParameter(3*j+3), peak.GetParError(3*j+3)) )
            print("A_{}   = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+1), peak.GetParError(3*j+1) ))
            print("mu_{}  = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+2), peak.GetParError(3*j+2) ))
            print("sig_{} = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+3), peak.GetParError(3*j+3) ))
        print("Chi^2 = {:=7.2f}".format( peak.GetChisquare() ))
        print("Chi^2/NDF = {:=7.2f}".format( peak.GetChisquare()/peak.GetNDF() ))
        print()

    plot_hist( spectrum, logy=False)
