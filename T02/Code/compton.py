import json
import numpy as np
from ROOT import TCanvas

import config as cfg
from histogram import Histogram
from finder import peak_fit
from calibrate import calibrate_known

cali = calibrate_known()

def analyse_spectrum( name, file_name, noise_file, peaks, plot=False, out=False ):
    canvas = TCanvas(name.format(""))
    canvas.Divide(1,3)

    opt_noise, noise = Histogram.Read( noise_file, name.format("Noise "), name.format("Noise "), calibration=cali )
    opt_hist, hist_raw = Histogram.Read( file_name, name.format("Spectrum "), name.format("Spectrum "), calibration=cali )
    canvas.cd(1)
    noise.Draw()

    canvas.cd(2)
    hist_raw.Draw()

    canvas.cd(3)
    #hist = hist_raw - opt_hist.realtime/opt_noise.realtime * noise
    hist = hist_raw - np.max(hist_raw.GetBinContents())/np.max(noise.GetBinContents()) * noise
    hist.Draw()
    canvas.Update()
    input()

    peak_fit( hist, peaks, plot=plot, out=out )
    hist.Draw()
    input()

def diff_cross_section( name, angles, noise, peaks, ring ):
    if ring:
        for angle in angles:
            r, l, n, file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle[0]) for peak in ps  ]
            analyse_spectrum( "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle[0]),
                    cfg.comp_r_dir+file_name, cfg.comp_r_dir+noise[l[0]],
                    angle_peaks, plot=True, out=True )

    else:
        for angle in angles:
            file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle) for peak in ps ]
            analyse_spectrum( "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle),
                    cfg.comp_c_dir+file_name, cfg.comp_c_dir+noise[angle],
                    angle_peaks, plot=True, out=True )

if __name__=="__main__":
    peaks = json.loads( open(cfg.data_dir+cfg.comp_peaks).read() )
    diff_cross_section( "Ring", cfg.ring_files, cfg.ring_noise, peaks["Ring"], True )
    diff_cross_section( "Conventional Alu", cfg.conv_files_Alu, cfg.conv_noise, peaks["Alu"], False  )
    diff_cross_section( "Conventional Steel", cfg.conv_files_Steel, cfg.conv_noise, peaks["Steel"], False  )
