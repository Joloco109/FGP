from reader import Hist
from calibrate import calibrate
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
leer_peaks_r = [
        "Leer_peaks.mca"]
leer_peaks_am = [
        "Leer_peaks.mca",
        "Leer_peaks1.mca"
        ]
boundries_r = (930,1450)
boundries_am = [(440,552), (1700,2100)] #552, 2100
paras = [ ( 5, 2e1, 5 ),
        ( 5, 1e1, 5 ),
        ( 5, 1e1, 1 )]
def leer(am):
    cali = calibrate( am )
    leer_peaks = []
    directory = data_dir + (am_dir if am else roe_dir)
    empty = Hist.read( directory + leer_names[ 1 if am else 0 ], "Leer", "Leermessung Americium" if am else "Leermessung Roehre", calibration=cali )
    if am:
        leer_peaks = leer_peaks_am
    else: 
        leer_peaks = leer_peaks_r
    
    for i in range(len(leer_peaks)):
        boundries = boundries_am[i] if am else boundries_r
        empty_peaks = Hist.read( directory + leer_peaks[i] , "Leer", "Leermessung Peaks Americium1" if am else "Leermessung Peaks Roehre", boundries=boundries ,calibration=cali )
        acc, height, fac = paras[ i+1 if am else 0 ]
        peaks = peak_fit( empty_peaks, accuracy=acc, peak_height=height, peak_fac=fac, max_peak_number = 4, plot_peaks=True)
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
        plot_hist( empty_peaks, logy=False)
    spectrum = Hist(empty.hist, "Spectrum", "Spectrum" )
    plot_hist( spectrum, logy=False)  
     

def main():
    print('Rö')
    leer(False)
    print('Am')
    leer(True)

    
if __name__ == "__main__":
    main()