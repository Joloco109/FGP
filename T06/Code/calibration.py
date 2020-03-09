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
            "Barium.mca",
            "Copper.mca",
            "Molybden.mca",
            "Rubidium.mca",
            "Silber.mca",
            "Stahl.mca",
            "Terbium.mca"
        ]
    ]

paras = [ ( 5, 1e2 ),
        ( 5, 1e2 )]

def calibrate( file_number, am ):
    directory = data_dir + (am_dir if am else roe_dir)
    empty = Hist.read( directory + leer_names[ 1 if am else 0 ], "Leer", "Leer" )
    spectrum = Hist.read( directory + calibration_names[ 1 if am else 0 ][file_number], "Spectrum_Noise", "Spectrum_Noise" )

    spectrum = Hist( spectrum.hist - empty.hist, "Spectrum", "Spectrum" )

    #plot_hist( spectrum )

    peaks = peak_fit( "gaus(0) + [3]", spectrum, accuracy=5, peak_height=1e2 )

    plot_hist( spectrum, logy=False )
