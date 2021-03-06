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

def mu( E, material, debug=False ):
    coeff = att_coeff[material]
    i = np.where(coeff[:,0]>E*1e-3)[0][0]
    mu = (coeff[i][1]-coeff[i-1][1])/(coeff[i][0]-coeff[i-1][0])*(E*1e-3-coeff[i][0]) + coeff[i][1]

    if debug:
        print("{:.2f}keV".format(E))
        print("\tmu_{: <5} = ({: >4.2e})cm^2/g".format( material, mu ))
        print("\tmu_{: <5} = ({: >4.2e})1/cm".format( material, mu*cfg.densities[material][0] ))
    return mu*cfg.densities[material][0]


def diff_cross_section_ring( N_e, s, R, ampl, sigma, E, E_prime, t ):
    r = np.sqrt(s[0]**2+R[0]**2)
    sig_r = 2/np.sqrt(s[0]**2+R[0]**2)*np.sqrt((s[0]*s[1])**2+(R[0]*R[1])**2)
    
    m = np.sqrt(2*np.pi)*sigma[0] * ampl[0]/t
    sig_m = m*np.sqrt((sigma[1]/sigma[0])**2+(ampl[1]/ampl[0])**2)

    mu_alu = mu( E, "Alu" )
    mu_alu_p = mu( E_prime, "Alu" )
    mu_air = mu( E, "Air" )
    mu_air_p = mu( E_prime, "Air" )

    eta = np.exp( -(mu_air+mu_air_p)*r -(mu_alu+mu_alu_p-mu_air-mu_air_p)*cfg.ring_thickness[0]/2 )
    sig_eta = eta * np.sqrt((-(mu_air+mu_air_p)*sig_r)**2+(-(mu_alu+mu_alu_p-mu_air-mu_air_p)*cfg.ring_thickness[1]/2)**2)

    N_e = (2*np.pi * R[0] * cfg.ring_thickness[0]**2 * cfg.densities["Alu"][0]*cfg.Z["Alu"]/(cfg.N["Alu"][0]*cfg.u),
            N_e[1] )
    
    print("Relative erorrs:")
    print("\tm  : {:.2f}".format(sig_m/m))
    print("\tr  : {:.2f}".format(sig_r/r))
    print("\tN  : {:.2f}".format(N_e[1]/N_e[0]))
    print("\teta: {:.2f}".format(sig_eta/eta))
    cross = 4*np.pi*r**4/( cfg.A[0]*cfg.I_gamma[0]*cfg.eff_conv[0]*N_e[0] * cfg.F_D_ring[0] ) * m / eta # cm^2
    sig_cross = cross*np.sqrt((sig_m/m)**2+(sig_eta/eta)**2+(N_e[1]/N_e[0])**2)
    sys_cross = cross*np.sqrt((cfg.A[1]/cfg.A[0])**2+(cfg.eff_conv[1]/cfg.eff_conv[0])**2+(cfg.F_D_ring[1]/cfg.F_D_ring[0])**2+(4*sig_r/r)**2)
    return ( cross, sig_cross, sys_cross )

def diff_cross_section_conv( ampl, sigma, E, E_prime, t, material ):
    m = np.sqrt(2*np.pi)*sigma[0] * ampl[0]/t
    sig_m = m*np.sqrt((sigma[1]/sigma[0])**2+(ampl[1]/ampl[0])**2)

    mu_mat = mu( E, material )
    mu_mat_p = mu( E_prime, material )
    mu_air = mu( E, "Air" )
    mu_air_p = mu( E_prime, "Air" )

    eta = np.exp( -mu_air*cfg.r_0_conv[0]-mu_air_p*cfg.r_conv[0] -(mu_mat+mu_mat_p-mu_air-mu_air_p)*cfg.d_conv[0]/2 )
    sys_eta = eta* np.sqrt((-mu_air*cfg.r_0_conv[1])**2+(-mu_air_p*cfg.r_conv[1])**2+(-(mu_mat+mu_mat_p-mu_air-mu_air_p)*cfg.d_conv[1]/2)**2)

    N_e = ( np.pi* cfg.d_conv[0]**2/4 * cfg.h_conv[0] * cfg.densities[material][0]*cfg.Z[material]/(cfg.N[material][0]*cfg.u),
            cfg.Ne_conv[material][1] )

    cross = 4*np.pi*cfg.r_0_conv[0]**2*cfg.r_conv[0]**2/( cfg.A[0]*cfg.I_gamma[0]*cfg.eff_conv[0]*N_e[0] * cfg.F_D_conv[0] ) * m / eta # cm^2
    sig_cross = cross*np.sqrt((N_e[1]/N_e[0])**2+(sig_m/m)**2)
    sys_cross = cross*np.sqrt((cfg.eff_conv[1]/cfg.eff_conv[0])**2+(cfg.A[1]/cfg.A[0])**2+(2*cfg.r_0_conv[1]/cfg.r_0_conv[0])**2+(2*cfg.r_conv[1]/cfg.r_conv[0])**2+(sys_eta/eta)**2+(cfg.F_D_conv[1]/cfg.F_D_conv[0])**2)
    return ( cross, sig_cross, sys_cross )


def analyse_spectrum( name, file_name, noise_file, peaks, plot=False, out=False, save=False ):
    opt_noise, noise = Histogram.Read( noise_file, name.format("Noise "), name.format("Noise "), calibration=cali )
    opt_hist, hist_raw = Histogram.Read( file_name, name.format("Spectrum "), name.format("Spectrum "), calibration=cali )
    #hist = hist_raw - opt_hist.realtime/opt_noise.realtime * noise
    hist = hist_raw - np.max(hist_raw.GetBinContents())/np.max(noise.GetBinContents()) * noise

    peaks = peak_fit( hist, peaks, brackground=False, plot=False, out=False )
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


def analyse_setup( name, angles, noise, peaks, key, plot=False, out=False, save=False ):
    angles_array = np.zeros(( len(angles), 2 ))
    amplitudes = np.zeros(( len(angles), 2 ))
    energies = np.zeros(( len(angles), 2 ))
    sigmas = np.zeros(( len(angles), 2 ))
    cross_section = np.zeros(( len(angles), 3 ))
    if key == "Ring":
        for i, angle in zip( range(len(angles)), angles):
            if out:
                print()
                print( name + " {:.0f}°".format(angle[0]) )
            r, l, n, file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle[0]) for peak in ps  ]
            t, a, e, s = analyse_spectrum(
                    "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle[0]),
                    cfg.comp_r_dir+file_name, cfg.comp_r_dir+noise[l[0]],
                    angle_peaks, plot=plot, out=out, save=save )
            if not len(e)==1:
                raise ValueError("You should have decided on exactly one peak for file by now!")
            angles_array[i] = angle
            amplitudes[i] = a[0]
            energies[i] = e[0]
            sigmas[i] = s[0]
            cross_section[i] = diff_cross_section_ring( n, l, r, a[0], s[0], 661, e[0][0], t )

    else:
        for i, angle in zip( range(len(angles)), angles):
            if out:
                print()
                print( name + " {:.0f}°".format(angle) )
            file_name = angles[angle]
            angle_peaks = [ tuple(peak) for ang, *ps in peaks if round(ang)==round(angle) for peak in ps ]
            t, a, e, s = analyse_spectrum(
                    "\\mbox{{{}"+name+" }}" + "{:.0f}^\\circ".format(angle),
                    cfg.comp_c_dir+file_name, cfg.comp_c_dir+noise[angle],
                    angle_peaks, plot=plot, out=out, save=save)
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

    all_graph = Graph( "Scattered photon energy",
            all_angles[:,0], all_energies[:,0],
            all_angles[:,1], all_energies[:,1] )
    func = Function( TF1("energy", "[0]/(1+[0]/[1]*(1-cos(pi*x/180)))") )
    func.function.SetParameter( 0, 661 )
    func.function.SetParLimits( 0, 0, 10e3 )
    func.function.SetParameter( 1, 512 )
    func.function.SetParLimits( 1, 0, 10e3 )
    legend.AddEntry(func.function, "E\mbox{ '}_\\gamma = E_\\gamma\mbox{ / }(1+\\frac{E_\\gamma}{m_e}(1-cos\\theta))")
    all_graph.Fit( func )
    paras = func.GetParameters()
    parErrs = func.GetParErrors()
    parErrSys = func.GetParErrorsSys()
    print("E_gamma   = {:6.2f} \\pm {:5.2f} \\pm {:5.2f}".format(paras[0], parErrs[0], parErrSys[0]))
    print("m_e       = {:6.2f} \\pm {:5.2f} \\pm {:5.2f}".format(paras[1], parErrs[1], parErrSys[1]))
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

def analyse_crosssection( keys, angles, crosssections, fix_ampl=False ):
    name = "diff_cross_"
    for k in keys:
        name += k + "_"
    canvas = TCanvas()
    if name == "diff_cross_Ring_Alu_Steel_":
        legend = TLegend(.65,.60,.97,.97)
    else:
        legend = TLegend(.52,.55,.89,.89)
    graphs = []
    graphs_sys = []
    all_angles = np.zeros(( sum([ len(a) for a in angles ]),2 ))
    all_crosssections = np.zeros(( sum([ len(a) for a in crosssections ]),3 ))
    i = 0
    for k, a, c in zip( keys, angles, crosssections):
        graphs.append( Graph( k, a[:,0], c[:,0] ) )
        index = np.logical_not(np.logical_or(a[:,0]==80, a[:,0]==90))
        a = a[index]
        c = c[index]
        if k=="Alu":
            a = a[:-1]
            c = c[:-1]
        graphs_sys.append([ Graph( k, a[:,0], c[:,0]+c[:,2] ),
                            Graph( k, a[:,0], c[:,0]-c[:,2] ) ])
        all_angles[i:i+len(a)] = a
        all_crosssections[i:i+len(a)] = c
        i += len(a)
    index = all_angles[:,0]!=0
    all_angles = all_angles[index]
    all_crosssections = all_crosssections[index]

    all_graph = Graph( "Diff. Cross-section",
            all_angles[:,0], all_crosssections[:,0],
            all_angles[:,1], all_crosssections[:,1],
            np.zeros(len(all_angles)), all_crosssections[:,2] )

    # rho = (1+[1]*(1-cos(pi*x/180)))
    func = Function( TF1("cross-section",
        "[0]*1/(1+[1]*(1-cos(pi*x/180)))^2 \
        * ( (1+[1]*(1-cos(pi*x/180))) +1/(1+[1]*(1-cos(pi*x/180))) -sin(pi*x/180)^2 )",
        0, 180 ) )
    func.function.SetParameter( 0, 3.88679483310156084179e1 )
    if fix_ampl:
        func.function.FixParameter( 0, 3.88679483310156084179e1 )
    func.function.SetParameter( 1, 661/512 )
    legend.AddEntry(func.function, "\\frac{d\\sigma}{d\\Omega}= \\frac{\\alpha^2\\lambda_e^2}{8\\pi\\rho^2}(\\rho+\\rho^{-1}-\\sin^2\\theta)")

    theo = Function( TF1("cross-section",
        "[0]*1/(1+[1]*(1-cos(pi*x/180)))^2 \
        * ( (1+[1]*(1-cos(pi*x/180))) +1/(1+[1]*(1-cos(pi*x/180))) -sin(pi*x/180)^2 )",
        0, 180 ) )
    theo.function.SetParameter( 0, 3.88679483310156084179e1 )
    theo.function.FixParameter( 0, 3.88679483310156084179e1 )
    theo.function.SetParameter( 1, 661/512 )
    theo.function.FixParameter( 1, 661/512 )
    theo.function.SetLineColor(1)
    theo.function.SetLineStyle(3)
    legend.AddEntry(theo.function, "\\frac{d\\sigma}{d\\Omega}_{theo}(\\theta)")

    all_graph.Draw(xName="\\theta [^\\circ]", yName="\\frac{d\\sigma}{d\\Omega} [mb]")
    colors = { "Ring":2, "Alu":3, "Steel":4 }

    all_graph.Fit( func, plot=False, out=False )
    paras = func.GetParameters()
    parErrs = func.GetParErrors()
    parErrSys = func.GetParErrorsSys()
    deltas = np.abs(paras-theo.GetParameters())/np.sqrt(parErrs**2+parErrSys**2)
    A = ( paras[0], parErrs[0], parErrSys[0] )
    a = ( paras[1], parErrs[1], parErrSys[1] )
    print("Ampl.  =({:5.2f} \\pm {:5.2f} \\pm {:5.2f})mb".format(paras[0], parErrs[0], parErrSys[0]))
    print("\\Delta = {:.2f} \\sigma".format(deltas[0]))
    print("E/m_e  = {:5.2f} \\pm {:5.2f} \\pm {:5.2f}".format(paras[1], parErrs[1], parErrSys[1]))
    print("\\Delta = {:.2f} \\sigma".format(deltas[1]))
    if func.GetNDF() == 0:
        print("Chi = {:4.2f}".format(func.GetChisquare()))
        print("You overfitted with laughable few data points!\nWhat did you expect?")
    else:
        print("Chi/Ndf = {:5.3f}".format(func.GetChisquare()/func.GetNDF()))

    all_graph.GetXaxis().SetLimits(0,120)
    all_graph.GetYaxis().SetLimits( 0, 2*A[0]+10 )
    all_graph.GetYaxis().UnZoom()
    func.function.Draw("LSame")
    theo.function.Draw("LSame")

    for g, k in zip(graphs, keys):
        g.graph.SetMarkerColor(colors[k])
        g.Draw("P", marker=3)
        legend.AddEntry(g.graph, k)

    for (gp, gm), k in zip(graphs_sys, keys):
        gp.graph.SetMarkerSize(0.5)
        gp.graph.SetMarkerColor(colors[k])
        gp.Draw("P", marker=2)
        gm.graph.SetMarkerSize(0.5)
        gm.graph.SetMarkerColor(colors[k])
        gm.Draw("P", marker=2)
    legend.Draw()
    canvas.Update()

    canvas.SaveAs( graph_dir + name + ".eps")
    input()

    return A, a

def total_crosssection( keys, angles, crosssections ):
    for k, a, c in zip( keys, angles, crosssections ):
        (A, sig_A, sys_A), (a, sig_a, sys_a) = analyse_crosssection( [k], [a], [c], fix_ampl=True )
        sigma_total = 4*np.pi*A/a**2 * ( (2+a*(1+a)*(8+a))/(1+2*a)**2+((a-1)**2-3)/(2*a)*np.log(1+2*a) )
        sig_sigma = np.sqrt(
                ( sigma_total * sig_A/A )**2
              + ( 4*np.pi*A *((8*a**5-20*a**4-90*a**3-95*a**2-40*a-6)*np.log(2*a+1)-4*a**5+78*a**4+126*a**3+68*a**2+12*a )/(2*a**4*(2*a+1)**3)* sig_a )**2
            )
        sys_sigma = np.sqrt(
                ( sigma_total * sys_A/A )**2
              + ( 4*np.pi*A *((8*a**5-20*a**4-90*a**3-95*a**2-40*a-6)*np.log(2*a+1)-4*a**5+78*a**4+126*a**3+68*a**2+12*a )/(2*a**4*(2*a+1)**3)* sys_a )**2
            )
        print(k+":")
        print("\t\\sigma = ({:6.2f} \\pm {:6.2f} \\pm {:6.2f})mb".format(sigma_total, sig_sigma, sys_sigma) )

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
        a, e, c = analyse_setup( name, file_name, noise_name, peaks[key], key, plot=False, out=True, save=True )
        angles.append(a)
        energies.append(e)
        cross_sections.append(c)

    analyse_energy( peaks, angles, energies )
    (A,_,_),(a,_,_) = analyse_crosssection( peaks, angles, cross_sections )
    sigma_total = 4*np.pi*A/a**2 * ( (2+a*(1+a)*(8+a))/(1+2*a)**2+((a-1)**2-3)/(2*a)*np.log(1+2*a) )
    print(sigma_total)
    total_crosssection( ["Alu","Steel"], angles[1:], cross_sections[1:] )
