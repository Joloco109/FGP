from reader import Hist
from calibrate import calibrate
from peakfinder import Peaks, peak_fit
from plot import plot_hist
from lit_values_reader import read_tabular, lit_file

data_dir = "Data/"
am_dir = "Am/"
roe_dir = "Röhre/"

leer_names = ["Leer.mca"]
element_names = ["Stahl.mca", "Chip.mca"]
boundries_s = (1200, 1350)
boundries_c = (910, 2300)
paras = [( 5, 1e1, 5 ), ( 5, 1e1, 5 )]

def element(am, cali=None, plot_peaks=False, txt_output=False):
    if cali==None:
        cali = calibrate(am)
    directory = data_dir + (am_dir if am else roe_dir)
    boundries = boundries_s if am else boundries_c
    
    empty_peaks = Hist.read( directory + leer_names[0] ,"Leer", "Leer Americium"if am else "Leer Roehre",  boundries=boundries ,calibration = cali)
    peaks_el = Hist.read( directory + element_names[0 if am else 1] , "Stahl"if am else "Chip", "Stahl Peaks Americium"if am else "Chip Peaks Roehre",  boundries=boundries ,calibration = cali)
    peaks_el = Hist( peaks_el.hist - empty_peaks.hist, "Peaks", "Stahl Peaks Americium" if am else "Chip Peaks Roehre")
    acc, height, fac = paras[0 if am else 1]
    peaks = peak_fit( peaks_el, accuracy=acc, peak_height=height, peak_fac=fac, max_peak_number = 4, plot_peaks=plot_peaks)
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
            print("Chi^2 = {:=7.2f}".format( peak.GetChisquare()))
            print("Chi^2/NDF = {:=7.2f}".format( peak.GetChisquare()/peak.GetNDF() ))
            print()
    if plot_peaks:
        plot_hist(peaks_el, logy=False)
    return energies, energy_res
     
def main():
    print('Am')
    element(True, plot_peaks=True, txt_output=True)
    print('Roe')
    element(False, plot_peaks=True, txt_output=True)

    
if __name__ == "__main__":
    main()
