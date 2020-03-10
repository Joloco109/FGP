from reader import Hist
from peakfinder import Peaks, peak_fit
from plot import plot_hist
from ctypes import c_double

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
            [ "Au" ],
            [ "Fe", "Mo", "Cr", "Ni" ]
        ],[
            [ "Cu" ],
            [ "Au" ],
            [ "Fe", "Mo", "Cr", "Ni" ],
            [ "Ba" ],
            [ "Mo" ],
            [ "Rb" ],
            [ "Tb" ]
        ]
    ]

paras = [ ( 5, 1e2 ),
        ( 5, 1e2 )]

def calibrate( file_number, am ):
    directory = data_dir + (am_dir if am else roe_dir)
    empty = Hist.read( directory + leer_names[ 1 if am else 0 ], "Leer", "Leer" )
    spectrum = Hist.read( directory + calibration_names[ 1 if am else 0 ][file_number], "Spectrum", "Spectrum" )
    elems = calibration_elements[1 if am else 0][file_number]

    spectrum = Hist( spectrum.hist - empty.hist, "Spectrum", "Spectrum" )

    peaks = peak_fit( spectrum, accuracy=5, peak_height=1e2 )

    energies = []
    energy_res = []

    for peak in peaks:
        print(peak)
        print("Chi^2 = {:=7.2f}".format( peak.GetChisquare() ))
        print("C     = {:=8.3f} +- {:=8.3f}".format( peak.GetParameter(0), peak.GetParError(0) ))
        for j in range(0, int((peak.GetNpar()-1)/3) ):
            energies.append( (peak.GetParameter(3*j+2), peak.GetParError(3*j+2)) )
            energy_res.append( (peak.GetParameter(3*j+3), peak.GetParError(3*j+3)) )
            print("A_{}   = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+1), peak.GetParError(3*j+1) ))
            print("mu_{}  = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+2), peak.GetParError(3*j+2) ))
            print("sig_{} = {:=8.3f} +- {:=8.3f}".format( j, peak.GetParameter(3*j+3), peak.GetParError(3*j+3) ))
        print()

    plot_hist( spectrum, logy=False )
