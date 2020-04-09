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
import compton

graph_dir = "Graphs/build/compton/e_mass/" 
cali = calibrate_known()
E_gamma = (661.657, 0.003)

def e_mass(energies, angles, energies_err, angles_err):
    e_graph = Graph( "Measurement of m_e", angles, energies, angles_err, energies_err)
    fit = Function( TF1( "electron mass", "pol1" ) )
    
    e_graph.Fit( fit, plot=True, out=True )
    canvas = TCanvas()
    legend = TLegend(.14,.82,.50,.89)
    legend.AddEntry(fit.function, "1/E^\mbox{'}_\\gamma-1/E_\\gamma = \\frac{1}{m_e}(1-\\cos\\theta)")
    e_graph.Draw(xName= "(1-\\cos\\theta)", yName="(1/E^\mbox{'}_\\gamma-1/E_\\gamma)[1/keV]")
    legend.Draw()
    input()
    paras = fit.GetParameters()
    parErrs = fit.GetParErrors()
    m_e = 1/paras[1]
    m_e_err = parErrs[1]/paras[1]**2
    print("m_e = ", m_e, " \pm ", m_e_err)
if __name__=="__main__":
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )
    peaks = json.loads( open(cfg.data_dir+cfg.comp_peaks).read() )
    angles = []
    energies = []
    en = []
    en_err = []
    an=[]
    an_err = []
    cross_sections = []
    for name, file_name, noise_name, key in zip(
                [ "Ring", "Conventional Alu", "Conventional Steel" ],
                [ cfg.ring_files, cfg.conv_files_Alu, cfg.conv_files_Steel ],
                [ cfg.ring_noise, cfg.conv_noise, cfg.conv_noise ],
                [ "Ring", "Alu", "Steel" ] ):
        a, e, c = compton.analyse_setup( name, file_name, noise_name, peaks[key], key )
        angles.append(a)
        energies.append(e)
        cross_sections.append(c)

    for a,b in zip(energies, angles):
        for [e,err] in a:
            en.append(1/e-1/E_gamma[0])
            en_err.append(np.sqrt((err/e**2)**2+(E_gamma[1]/E_gamma[0]**2)**2))
        for [a, err] in b:
            an.append(1-np.cos(np.pi*a/180))
            an_err.append(np.pi/180*np.sin(np.pi*a/180)*err)

    e_mass(en, an, en_err, an_err)