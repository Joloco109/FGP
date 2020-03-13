from reader import Hist
from calibrate import calibrate
from peakfinder import Peaks, peak_fit
from plot import plot_hist
from lit_values_reader import read_tabular, lit_file

data_dir = "Data/"
am_dir = "Am/"

leer_names = ["Leer.mca"]
stahl_names = ["Stahl.mca"]
stahl_peaks_am= ["Stahl_peak.mca"]
boundries = (1200, 1350)

paras = [( 5, 1e1, 5 ), ( 5, 1e1, 5 )]

def steel():
    cali = calibrate(True)
    directory = data_dir + (am_dir)
    empty = Hist.read( directory + leer_names[0], "Leer", "Leer", calibration = cali )
    steel = Hist.read( directory + stahl_names[0], "Stahl", "Stahl Americium",calibration = cali )
    
    spectrum = Hist(steel.hist, "Spectrum", "Spectrum" )
    plot_hist( spectrum, logy=False)
    spectrum = Hist( spectrum.hist - empty.hist, "Spectrum", "Spektrum Americium")
    plot_hist( spectrum, logy=False) 
    
    stahl_peaks = stahl_peaks_am
    
    for i in range(len(stahl_peaks)):
        steel_peaks = Hist.read( directory + stahl_peaks[i] , "Stahl", "Stahl Peaks Americium",  boundries=boundries ,calibration = cali) 
        acc, height, fac = paras[i]
        peaks = peak_fit( steel_peaks, accuracy=acc, peak_height=height, peak_fac=fac, max_peak_number = 4, plot_peaks=True)
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
        plot_hist( steel_peaks, logy=False)
     
def main():
    print('Am')
    steel()

    
if __name__ == "__main__":
    main()