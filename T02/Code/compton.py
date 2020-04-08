import json
import numpy as np
from ROOT import TCanvas

import config as cfg
from histogram import Histogram
from graph import Graph
from finder import peak_fit
from calibrate import calibrate_known

cali = calibrate_known()

def analyse_spectrum( name, file_name, noise_file, peaks, plot=False, out=False ):
    opt_noise, noise = Histogram.Read( noise_file, name.format("Noise "), name.format("Noise "), calibration=cali )
    opt_hist, hist_raw = Histogram.Read( file_name, name.format("Spectrum "), name.format("Spectrum "), calibration=cali )
    #hist = hist_raw - opt_hist.realtime/opt_noise.realtime * noise
    hist = hist_raw - np.max(hist_raw.GetBinContents())/np.max(noise.GetBinContents()) * noise

    if plot:
        canvas = TCanvas(name.format(""))
        canvas.Divide(1,3)
        canvas.cd(1)
        noise.Draw()
        canvas.cd(2)
        hist_raw.Draw()
        canvas.cd(3)
        hist.Draw()
        canvas.Update()
        input()

    peaks = peak_fit( hist, peaks, plot=plot, out=out )
    if plot:
        hist.Draw()
        input()

    paras = [ p.GetParameters() for p in peaks ]
    parErrs = [ p.GetParErrors() for p in peaks ]
    amplitudes = [ (p[2], pe[2]) for p, pe in zip(paras, parErrs) ]
    energies = [ (p[3], pe[3]) for p, pe in zip(paras, parErrs) ]
    std_deviations = [ (p[4], pe[4]) for p, pe in zip(paras, parErrs) ]
    if out:
        for i, a,e,s in zip( range(len(paras)), amplitudes, energies, std_deviations ):
            print("A_{} = {} \\pm {}".format( i, *a ))
            print("E_{} = {} \\pm {}".format( i, *e ))
            print("s_{} = {} \\pm {}".format( i, *s ))
            print()
    return amplitudes, energies, std_deviations

def diff_cross_section( name, angles, noise, peaks, ring ):
    angles_array = np.zeros(( len(angles), 2 ))
    amplitudes = np.zeros(( len(angles), 2 ))
    energies = np.zeros(( len(angles), 2 ))
    sigmas = np.zeros(( len(angles), 2 ))
    if ring:
        for i, angle in zip( range(len(angles)), angles):
            r, l, n, file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle[0]) for peak in ps  ]
            a, e, s = analyse_spectrum(
                    "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle[0]),
                    cfg.comp_r_dir+file_name, cfg.comp_r_dir+noise[l[0]],
                    angle_peaks, plot=False, out=True )
            if not len(e)==1:
                raise ValueError("You should have decided on exactly one peak for file by now!")
            angles_array[i] = angle
            amplitudes[i] = a[0]
            energies[i] = e[0]
            sigmas[i] = s[0]

    else:
        for i, angle in zip( range(len(angles)), angles):
            file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle) for peak in ps ]
            a, e, s = analyse_spectrum(
                    "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle),
                    cfg.comp_c_dir+file_name, cfg.comp_c_dir+noise[angle],
                    angle_peaks, plot=False, out=True )
            if not len(e)==1:
                raise ValueError("You should have decided on exactly one peak for file by now!")
            angles_array[i] = (angle, 1)
            amplitudes[i] = a[0]
            energies[i] = e[0]
            sigmas[i] = s[0]

    return angles_array, energies

def plot_energy( keys, angles, energies ):
    canvas = TCanvas()
    graphs = []
    all_angles = np.zeros(( sum([ len(a) for a in angles ]),2 ))
    all_energies = np.zeros(( sum([ len(a) for a in energies ]),2 ))
    i = 0
    for k, a, e in zip( keys, angles, energies):
        graphs.append( Graph( k, a[:,0], e[:,0], a[:,1], e[:,1] ) )
        all_angles[i:i+len(a)] = a
        all_energies[i:i+len(a)] = e
        i += len(a)

    all_graph = Graph( "Total", all_angles[:,0], all_energies[:,0], all_angles[:,1], all_energies[:,1] )
    all_graph.Draw()
    input()


if __name__=="__main__":
    peaks = json.loads( open(cfg.data_dir+cfg.comp_peaks).read() )
    angles = []
    energies = []
    for name, file_name, noise_name, key, ring in zip(
                [ "Ring", "Conventional Alu", "Conventional Steel" ],
                [ cfg.ring_files, cfg.conv_files_Alu, cfg.conv_files_Steel ],
                [ cfg.ring_noise, cfg.conv_noise, cfg.conv_noise ],
                [ "Ring", "Alu", "Steel" ],
                [ True, False, False ] ):
        a, e = diff_cross_section( name, file_name, noise_name, peaks[key], ring )
        angles.append(a)
        energies.append(e)

    plot_energy( peaks, angles, energies )
