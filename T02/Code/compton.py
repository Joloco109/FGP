import json
import numpy as np
from ROOT import TCanvas, TF1

import config as cfg
from histogram import Histogram
from function import Function
from graph import Graph
from finder import peak_fit
from calibrate import calibrate_known

cali = calibrate_known()

att_coeff = json.loads( open(cfg.data_dir+cfg.att_coeff).read() )
for key in att_coeff:
    att_coeff[key] = np.array(att_coeff[key])
# # [ *[E[MeV], mu[cm^2/g] ]


def diff_cross_section_ring( N_e, s, R, ampl, sigma, E, E_prime, t ):
    r = np.sqrt(s[0]**2+R[0]**2)
    m = np.sqrt(2*np.pi)*sigma[0] * ampl[0]/t

    coeff = att_coeff["Alu"]
    mu_alu = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e3)), 1 ]*cfg.densities["Alu"][0]
    mu_alu_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e3)), 1 ]*cfg.densities["Alu"][0]
    coeff = att_coeff["Air"]
    mu_air = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e3)), 1 ]*cfg.densities["Air"][0]
    mu_air_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e3)), 1 ]*cfg.densities["Air"][0]

    eta = np.exp( -(mu_air+mu_air_p)*r -(mu_alu+mu_alu_p-mu_air-mu_air_p)*cfg.ring_thickness[0]/2 )

    cross = 4*np.pi*r**4/( cfg.A[0]*cfg.I_gamma[0]*cfg.eff_conv[0]*N_e[0] * cfg.F_D_ring[0] ) * m / eta # cm^2
    return ( cross, 0, 0 )

def diff_cross_section_conv( ampl, sigma, E, E_prime, t, material ):
    m = np.sqrt(2*np.pi)*sigma[0] * ampl[0]/t

    coeff = att_coeff[material]
    mu_mat = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e3)), 1 ]*cfg.densities[material][0]
    mu_mat_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e3)), 1 ]*cfg.densities[material][0]
    coeff = att_coeff["Air"]
    mu_air = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e3)), 1 ]*cfg.densities["Air"][0]
    mu_air_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e3)), 1 ]*cfg.densities["Air"][0]

    eta = np.exp( -mu_air*cfg.r_0_conv[0]-mu_air_p*cfg.r_conv[0] -(mu_mat+mu_mat_p-mu_air-mu_air_p)*cfg.d_conv[0]/2 )

    cross = 4*np.pi*cfg.r_0_conv[0]**2*cfg.r_conv[0]**2/( cfg.A[0]*cfg.I_gamma[0]*cfg.eff_conv[0]*cfg.Ne_conv[material][0] * cfg.F_D_conv[0] ) * m / eta # cm^2
    return ( cross, 0, 0 )

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
    return opt_hist.time, amplitudes, energies, std_deviations

def analyse_setup( name, angles, noise, peaks, key ):
    angles_array = np.zeros(( len(angles), 2 ))
    amplitudes = np.zeros(( len(angles), 2 ))
    energies = np.zeros(( len(angles), 2 ))
    sigmas = np.zeros(( len(angles), 2 ))
    cross_section = np.zeros(( len(angles), 3 ))
    if key == "Ring":
        for i, angle in zip( range(len(angles)), angles):
            r, l, n, file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle[0]) for peak in ps  ]
            t, a, e, s = analyse_spectrum(
                    "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle[0]),
                    cfg.comp_r_dir+file_name, cfg.comp_r_dir+noise[l[0]],
                    angle_peaks, plot=False, out=True )
            if not len(e)==1:
                raise ValueError("You should have decided on exactly one peak for file by now!")
            angles_array[i] = angle
            amplitudes[i] = a[0]
            energies[i] = e[0]
            sigmas[i] = s[0]
            cross_section[i] = diff_cross_section_ring( n, l, r, a[0], s[0], 661, e[0][0], t )

    else:
        for i, angle in zip( range(len(angles)), angles):
            file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle) for peak in ps ]
            t, a, e, s = analyse_spectrum(
                    "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle),
                    cfg.comp_c_dir+file_name, cfg.comp_c_dir+noise[angle],
                    angle_peaks, plot=False, out=True )
            if not len(e)==1:
                raise ValueError("You should have decided on exactly one peak for file by now!")
            angles_array[i] = (angle, 1)
            amplitudes[i] = a[0]
            energies[i] = e[0]
            sigmas[i] = s[0]
            cross_section[i] = diff_cross_section_conv( a[0], s[0], 661, e[0][0], t, key )

    cross_section *= 1e24 # barn
    cross_section *= 1e6  # mubarn
    return angles_array, energies, cross_section

def analyse_energy( keys, angles, energies ):
    canvas = TCanvas()
    graphs = []
    all_angles = np.zeros(( sum([ len(a) for a in angles ]),2 ))
    all_energies = np.zeros(( sum([ len(a) for a in energies ]),2 ))
    i = 0
    for k, a, e in zip( keys, angles, energies):
        graphs.append( Graph( k, a[:,0], e[:,0] ) )
        all_angles[i:i+len(a)] = a
        all_energies[i:i+len(a)] = e
        i += len(a)

    all_graph = Graph( "Total", all_angles[:,0], all_energies[:,0], all_angles[:,1], all_energies[:,1] )
    func = Function( TF1("energy", "[0]/(1+[0]/[1]*(1-cos(pi*x/180)))") )
    func.function.SetParameter( 0, 661 )
    func.function.SetParLimits( 0, 0, 10e3 )
    func.function.SetParameter( 1, 512 )
    func.function.SetParLimits( 1, 0, 10e3 )

    all_graph.Fit( func )
    paras = func.GetParameters()
    parErrs = func.GetParErrors()
    print("E_gamma   = {:.2f} \\pm {:.2f}".format(paras[0], parErrs[0]))
    print("m_e       = {:.2f} \\pm {:.2f}".format(paras[1], parErrs[1]))
    print("Chi^2/NdF = {:.2f}".format( func.GetChisquare()/func.GetNDF() ) )

    all_graph.Draw()
    colors = { "Ring":2, "Alu":3, "Steel":4 }
    for g, k in zip(graphs, keys):
        g.graph.SetMarkerColor(colors[k])
        g.Draw("P", marker =3)
    input()

def analyse_crosssection( keys, angles, crosssections ):
    canvas = TCanvas()
    graphs = []
    all_angles = np.zeros(( sum([ len(a) for a in angles ]),2 ))
    all_crosssections = np.zeros(( sum([ len(a) for a in crosssections ]),3 ))
    i = 0
    for k, a, e in zip( keys, angles, crosssections):
        graphs.append( Graph( k, a[:,0], e[:,0] ) )
        all_angles[i:i+len(a)] = a
        all_crosssections[i:i+len(a)] = e
        i += len(a)

    all_graph = Graph( "Total", all_angles[:,0], all_crosssections[:,0], all_angles[:,1], all_crosssections[:,1] )

    all_graph.Draw()
    colors = { "Ring":2, "Alu":3, "Steel":4 }
    for g, k in zip(graphs, keys):
        g.graph.SetMarkerColor(colors[k])
        g.Draw("P", marker =3)
    input()


if __name__=="__main__":
    peaks = json.loads( open(cfg.data_dir+cfg.comp_peaks).read() )
    angles = []
    energies = []
    cross_sections = []
    for name, file_name, noise_name, key in zip(
                [ "Ring", "Conventional Alu", "Conventional Steel" ],
                [ cfg.ring_files, cfg.conv_files_Alu, cfg.conv_files_Steel ],
                [ cfg.ring_noise, cfg.conv_noise, cfg.conv_noise ],
                [ "Ring", "Alu", "Steel" ] ):
        a, e, c = analyse_setup( name, file_name, noise_name, peaks[key], key )
        angles.append(a)
        energies.append(e)
        cross_sections.append(c)

    analyse_energy( peaks, angles, energies )
    analyse_crosssection( peaks, angles, cross_sections )
