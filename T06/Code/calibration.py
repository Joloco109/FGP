from reader import Hist
from peakfinder import Peaks, peak_fit
from plot import plot_hist, plot_graph
from lit_values_reader import read_tabular, lit_file
from graph import Graph

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

calibration_peaks = [ [
            [ "KL3", "KM3" ],
            [ "L3M5", "L2M5", "KL2", "KM2", "KN1", None, None, None ],
            [ None,None,None,None,None,None,None,None,None,None ]
        ],[
            [ "KL3", "KM3" ],
            [ "KL3", "KM3", "KN3" ],
            [ None ],
            [ None,"KL2", "KL3", "KM3", "KN3" ],
            [ "KL3", "KM2" ],
            [ "KL2", "KM2" ],
            [ "L3M4", "L2M4", "L3N4", "KL2", "KL3", None ] #"KM3" ]
        ]
    ]

paras = [ ( 5, 1.5e2, 5 ),
        ( 5, 5e1, 5 )]

def calibrate_file( file_number, am, ohne_leer=True, show_spectral_lines=False ):
    file_name = calibration_names[ 1 if am else 0 ][file_number]
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
        print(calibration_peaks[ 1 if am else 0 ][file_number])
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

    acc, height, fac = paras[ 1 if am else 0 ]
    peaks = peak_fit( spectrum, accuracy=acc, peak_height=height, peak_fac=fac)
    print()

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

    return energies, energies_theo, energy_res

def calibrate( am ):
    energies = []
    energies_theo = []
    for i in range(len(calibration_names[ 1 if am else 0 ])):
        e, e_theo, e_res = calibrate_file( i, am )
        e = [ (e1, e2) for e1, e2 in zip( e, e_theo) if not e2 == None ]
        e.sort(key=lambda x : x[0])
        e_theo = [ x[1] for x in e ]
        e = [ x[0] for x in e ]

        energies += e
        energies_theo += e_theo
    calibration = Graph( energies, energies_theo )
    calibration.fit( "pol1" )
    plot_graph( calibration )

def main():
    print("Am:")
    calibrate( True )
    print()
    print()

    print("Rö:")
    calibrate( False )
    print()
    print()

if __name__ == "__main__":
    main()
