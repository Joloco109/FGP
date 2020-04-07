import numpy as np
import os
from ROOT import TCanvas,TLegend, TF1, TMarker
import json

from calibration import Calibration
from function import Function
import calibrate
from histogram import Histogram
from graph import Graph
import config as cfg
from finder import find_edges, peak_fit, edge_fit

graph_dir = "Graphs/build/efficiency/" 
peak_area = [(580, 730)]
I =[0.9989,0.9991,0.805,0.2858, 0.075583, 0.265, 0.12942, 0.14605, 0.12005,0.8979]

def efficiency_one( plot=False, out=False, save=False ):
    cali = calibrate.calibrate_known()
    
    opt_noise, noise = Histogram.Read( cfg.eff_dir+cfg.eff_files[0], "noise", "noise measurement", calibration = cali  )
    opt, hist = Histogram.Read( cfg.eff_dir+cfg.eff_files[1], "eff", "efficiency measurement", calibration = cali )
    hist -= opt.time / opt_noise.time * noise
    
    peak_fits = peak_fit( hist, peak_area, plot=False, out=False)
    for f in peak_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            if out:
                for i,j in zip(paras, sig_paras):
                    print(i,"\pm",j)
    if plot:
        canvas = TCanvas("canvas","canvas")
        hist.Draw(xName="Energie/keV", yName="counts")
        for f in peak_fits:
            f.function.SetLineColor(2)
            f.function.Draw("Same")
            input()
    m = paras[2]*paras[4]*np.sqrt(2*np.pi)/opt.time
    m_err = np.sqrt((paras[4]*np.sqrt(2*np.pi)*sig_paras[2])**2+(paras[2]*np.sqrt(2*np.pi)*sig_paras[4])**2)/opt.time
    eff = 4*np.pi*cfg.r[0]**2*m/(cfg.A[0]*cfg.I_gamma[0]*cfg.F_D[0])
    eff_err = eff*np.sqrt((m_err/m)**2+(cfg.A[1]/cfg.A[0])**2+(cfg.r[1]/cfg.r[0])**2+(cfg.F_D[1]/cfg.F_D[0])**2)
    print(m, " \pm ", m_err)
    print(eff, " \pm ", eff_err)
    if save:
        canvas.SaveAs( graph_dir + "efficiency_60Co.eps" )
        input()
    return eff, eff_err, paras[3], sig_paras[3]

def efficiency( plot=False, out=False, save=False ):
    cali = calibrate.calibrate_known()
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "noise measurement",calibration=cali )

    data = json.loads( open( cfg.cali_dir+cfg.cali_extrema ).read() )
    
    peaks = []
    for [element_name, candidates] in data:
        (
            hist,
            (back_edges_fits, back_pos),
            (comp_edges_fits, comp_pos),
            (peak_fits, peak_pos)
        ) = calibrate.analyse_element( element_name, candidates, (opt_rausch, rausch), cali=cali, out=False )
        
        peaks.append((peak_fits,peak_pos))

    fun = []
    energ = []
    energ_err = []

    for (f,value) in peaks:    
        for i in range(len(f)):
            fun.append(f[i])
        for (en,err) in value:
            energ.append(en)
            energ_err.append(err)
    energ.append(e_gamma)   
    energ_err.append(e_gamma_err)
    func = np.delete(fun, [0,3,4,6,7,9,14,16])
    energies = np.delete(energ, [0,3,4,6,7,9,14,16])
    energies_err = np.delete(energ_err, [0,3,4,6,7,9,14,16])
    efficiencys = []
    efficiencys_err = []
    i = 0
    for f,e in zip(func, energies):
        paras = f.GetParameters()
        sig_paras = f.GetParErrors()
        
        m = paras[2]*paras[4]*np.sqrt(2*np.pi)/600
        m_err = np.sqrt((paras[4]*np.sqrt(2*np.pi)*sig_paras[2])**2+(paras[2]*np.sqrt(2*np.pi)*sig_paras[4])**2)/600
        eff = 4*np.pi*cfg.r[0]**2*m/(cfg.A[0]*I[i]*cfg.F_D[0])
        eff_err = eff*np.sqrt((m_err/m)**2+(cfg.A[1]/cfg.A[0])**2+(cfg.r[1]/cfg.r[0])**2+(cfg.F_D[1]/cfg.F_D[0])**2)
        efficiencys.append(eff)
        efficiencys_err.append(eff_err)
        i += 1
        
    efficiencys.append(effi)
    efficiencys_err.append(effi_err)
    eff_graph = Graph( "Efficiency measurement", energies, efficiencys, energies_err, efficiencys_err )
    eff_f = Function( TF1( "Calibration", "pol1" ) )
    eff_graph.Fit( eff_f, plot=plot, out=out )
    
    if out:
        print("Efficiency:")
        print("\tb = {:.5f} \\pm {:.5f}".format(eff_f.GetParameters()[0], eff_f.GetParErrors()[0]))
        print("\ta      = {:.5f} \\pm {:.5f}".format(eff_f.GetParameters()[1], eff_f.GetParErrors()[1]))
        print("\tChi^2/NdF = {:.3f}".format(eff_f.GetChisquare()/eff_f.GetNDF()))

    if plot:
        canvas = TCanvas("canvas","canvas")
        legend = TLegend(.63,.79,.89,.89)
        eff_graph.Draw(xName = "Energy [keV]", yName = "Efficiency")
        legend.AddEntry(cali.function, "\\epsilon = a E_\\gamma - b")
        legend.Draw()
        if save:
            canvas.SaveAs( graph_dir + "efficency.eps" )
        input()
    
if __name__ == "__main__":
    
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )
    effi, effi_err, e_gamma, e_gamma_err = efficiency_one( False, False, False)
    efficiency( True, True, True)
