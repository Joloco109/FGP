import json
import os
import numpy as np
from ROOT import TCanvas, TF1, gStyle, TLegend

import config as cfg
from histogram import Histogram
from function import Function
from graph import Graph
from finder import peak_fit
from calibrate import calibrate_known

graph_dir = "Graphs/build/compton/spectra/" 
cali = calibrate_known()


att_coeff = json.loads( open(cfg.data_dir+cfg.att_coeff).read() )
for key in att_coeff:
    att_coeff[key] = np.array(att_coeff[key])
# # [ *[E[MeV], mu[cm^2/g] ]


def diff_cross_section_ring( N_e, s, R, ampl, sigma, E, E_prime, t ):
    r = np.sqrt(s[0]**2+R[0]**2)
    sig_r = 2/np.sqrt(s[0]**2+R[0]**2)*np.sqrt((s[0]*s[1])**2+(R[0]*R[1])**2)
    
    m = np.sqrt(2*np.pi)*sigma[0] * ampl[0]/t
    sig_m = m*np.sqrt((sigma[1]/sigma[0])**2+(ampl[1]/ampl[0])**2)

    coeff = att_coeff["Alu"]
    mu_alu = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e-3)), 1 ]*cfg.densities["Alu"][0]
    mu_alu_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e-3)), 1 ]*cfg.densities["Alu"][0]
    coeff = att_coeff["Air"]
    mu_air = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e-3)), 1 ]*cfg.densities["Air"][0]
    mu_air_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e-3)), 1 ]*cfg.densities["Air"][0]

    eta = np.exp( -(mu_air+mu_air_p)*r -(mu_alu+mu_alu_p-mu_air-mu_air_p)*cfg.ring_thickness[0]/2 )
    sig_eta = eta * np.sqrt((-(mu_air+mu_air_p)*sig_r)**2+(-(mu_alu+mu_alu_p-mu_air-mu_air_p)*cfg.ring_thickness[1]/2)**2)
    
    cross = 4*np.pi*r**4/( cfg.A[0]*cfg.I_gamma[0]*cfg.eff_conv[0]*N_e[0] * cfg.F_D_ring[0] ) * m / eta # cm^2
    sig_cross = cross*np.sqrt((4*sig_r/r)**2+(N_e[1]/N_e[0])**2+(sig_m/m)**2+(sig_eta/eta)**2)
    sys_cross = cross*np.sqrt((cfg.A[1]/cfg.A[0])**2+(cfg.eff_conv[1]/cfg.eff_conv[0])**2+(cfg.F_D_ring[1]/cfg.F_D_ring[0])**2)
    return ( cross, sig_cross, sys_cross )

def diff_cross_section_conv( ampl, sigma, E, E_prime, t, material ):
    m = np.sqrt(2*np.pi)*sigma[0] * ampl[0]/t
    sig_m = m*np.sqrt((sigma[1]/sigma[0])**2+(ampl[1]/ampl[0])**2)

    coeff = att_coeff[material]
    mu_mat = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e-3)), 1 ]*cfg.densities[material][0]
    mu_mat_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e-3)), 1 ]*cfg.densities[material][0]
    coeff = att_coeff["Air"]
    mu_air = coeff[ np.argmin(np.abs(coeff[:,0]-E*1e-3)), 1 ]*cfg.densities["Air"][0]
    mu_air_p = coeff[ np.argmin(np.abs(coeff[:,0]-E_prime*1e-3)), 1 ]*cfg.densities["Air"][0]

    eta = np.exp( -mu_air*cfg.r_0_conv[0]-mu_air_p*cfg.r_conv[0] -(mu_mat+mu_mat_p-mu_air-mu_air_p)*cfg.d_conv[0]/2 )
    sys_eta = eta* np.sqrt((-mu_air*cfg.r_0_conv[1])**2+(-mu_air_p*cfg.r_conv[1])**2+(-(mu_mat+mu_mat_p-mu_air-mu_air_p)*cfg.d_conv[1]/2)**2)

    cross = 4*np.pi*cfg.r_0_conv[0]**2*cfg.r_conv[0]**2/( cfg.A[0]*cfg.I_gamma[0]*cfg.eff_conv[0]*cfg.Ne_conv[material][0] * cfg.F_D_conv[0] ) * m / eta # cm^2
    sig_cross = cross*np.sqrt((cfg.Ne_conv[material][1]/cfg.Ne_conv[material][0])**2+(sig_m/m)**2)
    sys_cross = cross*np.sqrt((cfg.eff_conv[1]/cfg.eff_conv[0])**2+(cfg.A[1]/cfg.A[0])**2+(2*cfg.r_0_conv[1]/cfg.r_0_conv[0])**2+(2*cfg.r_conv[1]/cfg.r_conv[0])**2+(sys_eta/eta)**2+(cfg.F_D_conv[1]/cfg.F_D_conv[0])**2)
    return ( cross, sig_cross, sys_cross )


def analyse_spectrum( name, file_name, noise_file, peaks, plot=False, out=False, save=False ):
    opt_noise, noise = Histogram.Read( noise_file, name.format("Noise "), name.format("Noise "), calibration=cali )
    opt_hist, hist_raw = Histogram.Read( file_name, name.format("Spectrum "), name.format("Spectrum "), calibration=cali )
    #hist = hist_raw - opt_hist.realtime/opt_noise.realtime * noise
    hist = hist_raw - np.max(hist_raw.GetBinContents())/np.max(noise.GetBinContents()) * noise

    peaks = peak_fit( hist, peaks, brackground=False, plot=False, out=out )
    paras = [ p.GetParameters() for p in peaks ]
    parErrs = [ p.GetParErrors() for p in peaks ]
    amplitudes = [ (p[2], pe[2]) for p, pe in zip(paras, parErrs) ]
    energies = [ (p[3], pe[3]) for p, pe in zip(paras, parErrs) ]
    std_deviations = [ (p[4], pe[4]) for p, pe in zip(paras, parErrs) ]
    if out:
        for i, a,e,s in zip( range(len(paras)), amplitudes, energies, std_deviations ):
            print("A_{} = {: >4.2e} \\pm {: >4.2e}".format( i, *a ))
            print("E_{} = {: >8.3f} \\pm {: >8.3f}".format( i, *e ))
            print("s_{} = {: >8.3f} \\pm {: >8.3f}".format( i, *s ))
            print("m_{} = {: >4.2e} \\pm {: >4.2e}".format( i, np.sqrt(2*np.pi)*a[0]*s[0], np.sqrt(2*np.pi*( (a[0]*s[1])**2+(a[1]*s[0])**2 )) ))
            print()

    if plot:
        canvas = TCanvas(name.format(""))
        canvas.Divide(1,2)
        canvas.cd(1)
        gStyle.SetOptStat(0)
        hist_raw.hist.SetNameTitle(name.format("Spectrum with noise, "),name.format("Spectrum with noise, "))
        hist_raw.hist.SetAxisRange(0, 800)
        hist_raw.hist.SetTitleSize(0.05, "X")
        hist_raw.hist.SetLabelSize(0.05, "X")
        hist_raw.hist.SetTitleSize(0.06, "Y")
        hist_raw.hist.SetLabelSize(0.06, "Y")
        hist_raw.hist.SetTitleOffset(0.8, "Y")
        hist_raw.Draw()
        canvas.cd(2)
        gStyle.SetOptStat(0)
        legend = TLegend(.63,.14,.89,.26)
        legend.AddEntry(peaks[0].function, "scattered photo peak fit")
        legend.AddEntry(peaks[0].function, "\tChi^2/NdF = {:.3f}".format(peaks[0].GetChisquare()/peaks[0].GetNDF()))
        hist.hist.SetNameTitle(name.format("Spectrum "), name.format("Spectrum "))
        hist.hist.SetAxisRange(0, 800)
        hist.hist.SetTitleSize(0.05, "X")
        hist.hist.SetLabelSize(0.05, "X")
        hist.hist.SetTitleSize(0.06, "Y")
        hist.hist.SetLabelSize(0.06, "Y")
        hist.hist.SetTitleOffset(0.8, "Y")
        hist.Draw()
        for p in peaks:
            p.function.Draw("Same")
        legend.Draw()
        canvas.Update()
        if save:
            canvas.SaveAs( graph_dir + file_name.split("/")[-1][:-4] + ".eps" )
        input()

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
                    angle_peaks, plot=False, out=True, save=True )
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
                    angle_peaks, plot=False, out=True, save=True )
            if not len(e)==1:
                raise ValueError("You should have decided on exactly one peak for file by now!")
            angles_array[i] = (angle, 1)
            amplitudes[i] = a[0]
            energies[i] = e[0]
            sigmas[i] = s[0]
            cross_section[i] = diff_cross_section_conv( a[0], s[0], 661, e[0][0], t, key )

    cross_section *= 1e24 # barn
    cross_section *= 1e3  # mbarn
    return angles_array, energies, cross_section

def analyse_energy( keys, angles, energies ):
    canvas = TCanvas()
    legend = TLegend(.47,.65,.89,.89)
    graphs = []
    all_angles = np.zeros(( sum([ len(a) for a in angles ]),2 ))
    all_energies = np.zeros(( sum([ len(a) for a in energies ]),2 ))
    i = 0
    for k, a, e in zip( keys, angles, energies):
        graphs.append( Graph( k, a[:,0], e[:,0] ) )
        all_angles[i:i+len(a)] = a
        all_energies[i:i+len(a)] = e
        i += len(a)

    all_graph = Graph( "Scattered photon energy", all_angles[:,0], all_energies[:,0], all_angles[:,1], all_energies[:,1] )
    func = Function( TF1("energy", "[0]/(1+[0]/[1]*(1-cos(pi*x/180)))") )
    func.function.SetParameter( 0, 661 )
    func.function.SetParLimits( 0, 0, 10e3 )
    func.function.SetParameter( 1, 512 )
    func.function.SetParLimits( 1, 0, 10e3 )
    legend.AddEntry(func.function, "E\mbox{ '}_\\gamma = E_\\gamma\mbox{ / }(1+\\frac{E_\\gamma}{m_e}(1-cos\\theta))")
    all_graph.Fit( func )
    paras = func.GetParameters()
    parErrs = func.GetParErrors()
    print("E_gamma   = {:.2f} \\pm {:.2f}".format(paras[0], parErrs[0]))
    print("m_e       = {:.2f} \\pm {:.2f}".format(paras[1], parErrs[1]))
    print("Chi^2/NdF = {:.2f}".format( func.GetChisquare()/func.GetNDF() ) )
    
    all_graph.Draw(xName="\\theta [^\\circ]", yName="E\mbox{ '}_\\gamma [keV]")
    colors = { "Ring":6, "Alu":3, "Steel":4 }

    for g, k in zip(graphs, keys):
        g.graph.SetMarkerColor(colors[k])
        g.Draw("P", marker=3)
        legend.AddEntry(g.graph, k)
    legend.Draw()
    canvas.SaveAs( graph_dir + "compton.eps" )
    input()

def analyse_crosssection( keys, angles, crosssections ):
    canvas = TCanvas()
    legend = TLegend(.47,.65,.89,.89)
    graphs = []
    all_angles = np.zeros(( sum([ len(a) for a in angles ]),2 ))
    all_crosssections = np.zeros(( sum([ len(a) for a in crosssections ]),3 ))
    i = 0
    for k, a, c in zip( keys, angles, crosssections):
        graphs.append( Graph( k, a[:,0], c[:,0] ) )
        all_angles[i:i+len(a)] = a
        all_crosssections[i:i+len(a)] = c
        i += len(a)

    all_graph = Graph( "Diff. Cross-section", all_angles[:,0], all_crosssections[:,0], all_angles[:,1], all_crosssections[:,1] )
    # rho = (1+a[1]*(1-cos(pi*x/180)))
    func = Function( TF1("cross-section", "[0]*1/(1+[1]*(1-cos(pi*x/180)))^2 * ( (1+[1]*(1-cos(pi*x/180))) +1/(1+[1]*(1-cos(pi*x/180))) -sin(pi*x/180)^2 )", 0, 180 ) )
    func.function.SetParameter( 0, 3.97248068393825954558e1 )
    func.function.FixParameter( 0, 3.97248068393825954558e1 )
    func.function.SetParameter( 1, 661/512 )
    func.function.FixParameter( 1, 661/512 )
    legend.AddEntry(func.function, "\\frac{d\\sigma}{d\\Omega}")

    all_graph.Draw(xName="\\theta [^\\circ]", yName="\\frac{d\\sigma}{d\\Omega} [mb]")
    colors = { "Ring":2, "Alu":3, "Steel":4 }

    func.function.Draw("LSame")

    for g, k in zip(graphs, keys):
        g.graph.SetMarkerColor(colors[k])
        g.Draw("P", marker=3)
        legend.AddEntry(g.graph, k)
    legend.Draw()
    canvas.Update()
    input()


if __name__=="__main__":
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )
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
