from identifier import identify_file
from recalibrate import calibrate_bayesian
from parameter import calibration_lines

def identify(file_number, am, cali=None, trans=None, ohne_leer=True, plot_peaks=True, txt_output=True):
    if cali == None:
        cali = calibrate_bayesian( am )
    if trans == None:
        trans = calibration_lines[1 if am else 0][file_number]
    return identify_file( file_number, am, cali=cali, trans=trans,
            ohne_leer=ohne_leer, plot_peaks=plot_peaks, txt_output=txt_output)
