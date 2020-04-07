import json
import numpy as np
import os
from ROOT import TCanvas,TLegend, TF1, TMarker, TLine

from histogram import Histogram
from graph import Graph
from function import Function
from calibration import Calibration
import config as cfg
from finder import find_edges, peak_fit, edge_fit
import calibrate

graph_dir = "Graphs/build/e_mass/" 

peak_area = [(450, 565)]

def mass(plot=True, out=True, save=True):
    cali = calibrate.calibrate_known()
    
    opt_noise, noise = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "noise", "noise measurement", calibration = cali  )
    opt, hist = Histogram.Read( cfg.cali_dir+"22Na calibration.TKA", "22Na", "22Na", calibration=cali )
    hist -= opt.time / opt_noise.time * noise
    
    peak_fits = peak_fit( hist, peak_area, plot=True, out=True)
    print(peak_fits)
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
    if save:
        canvas.SaveAs( graph_dir + "e_mass.eps" )
        input()
def mass_improved(plot=True, out=True, save=True):
    cali = calibrate.calibrate_known()
    
    opt_noise, noise = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "noise", "noise measurement", calibration = cali  )
    opt, hist = Histogram.Read( cfg.cali_dir+"22Na calibration.TKA", "22Na", "22Na", calibration=cali )
    hist -= opt.time / opt_noise.time * noise
    
    candidates = [["B_edge", [110, 170] ], ["C_edge", [200, 260]], ["peak", [300,380]] ]
    hist,(back_edges_fits, back_pos),(comp_edges_fits, comp_pos),(peak_fits, peak_pos) = calibrate.analyse_element("22Na", candidates, (opt_noise, noise), cali=cali, out=True)
    
    if plot:
        canvas = TCanvas("canvas","canvas")
        hist.Draw(xName="channel number", yName="counts")
        legend = TLegend(.70,.30,.89,.51)
        legend.AddEntry(hist.hist, "Data")
        edges = []
        to_legend=True
        for f in back_edges_fits:
            f.function.SetLineColor(3)
            f.function.Draw("Same")
            if to_legend:
                legend.AddEntry(f.function, "backscatter fit")
                to_legend=False
            p = f.GetParameters()
            e = TLine( p[2]-p[3], p[0], p[2]-p[3], p[0]+p[1]*2*p[3] )
            e.SetLineColor(3)
            e.SetLineWidth(2)
            e.Draw()
            edges.append(e)
        to_legend=True
        for f in comp_edges_fits:
                f.function.SetLineColor(6)
                f.function.Draw("Same")
                if to_legend:
                    legend.AddEntry(f.function, "compton fit")
                    to_legend=False
                p = f.GetParameters()
                e = TLine( p[2]+p[3], p[0], p[2]+p[3], p[0]+p[1]*2*p[3] )
                e.SetLineColor(6)
                e.SetLineWidth(2)
                e.Draw()
                edges.append(e)
        to_legend=True
        for f in peak_fits:
                f.function.SetLineColor(2)
                f.function.Draw("Same")
                if to_legend:
                    legend.AddEntry(f.function, "peak fit")
                    to_legend=False
        legend.Draw()
        if save:
                canvas.SaveAs( graph_dir + "e_mass_imp" + ".eps" )
        input()
    
if __name__ == "__main__":
    
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )
        
    mass_improved()
