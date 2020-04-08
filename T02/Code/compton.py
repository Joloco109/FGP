import numpy as np
from ROOT import TCanvas

import config as cfg
from histogram import Histogram
from calibrate import calibrate_known

cali = calibrate_known()

def analyse_spectrum( name, file_name, noise_file ):
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

def diff_cross_section( name, angles, noise, ring ):
    if ring:
        for angle in angles:
            r, l, n, file_name = angles[angle]
            analyse_spectrum( "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle[0]),
                    cfg.comp_r_dir+file_name, cfg.comp_r_dir+noise[l[0]] )

    else:
        for angle in angles:
            file_name = angles[angle]
            analyse_spectrum( "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle),
                    cfg.comp_c_dir+file_name, cfg.comp_c_dir+noise[angle] )

if __name__=="__main__":
    diff_cross_section( "Ring", cfg.ring_files, cfg.ring_noise, True )
    diff_cross_section( "Conventional Alu", cfg.conv_files_Alu, cfg.conv_noise, False  )
    diff_cross_section( "Conventional Steel", cfg.conv_files_Steel, cfg.conv_noise, False  )
