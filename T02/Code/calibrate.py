import json
import numpy as np
import os

from ROOT import TCanvas,TLegend
from calibration import Calibration
from histogram import Histogram
import config as cfg
from finder import find_edges, peak_fit, edge_fit

graph_dir = "Graphs/build/calibrate/"

def calibrate_known( plot=False, out=False, save=False ):
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "noise measurement" )
    canvas = TCanvas("canvas","canvas")
    rausch.Draw(xName="channel number", yName="counts")
    canvas.SaveAs( graph_dir + "noise.eps" )
    input()

    data = json.loads( open( cfg.cali_dir+cfg.cali_extrema ).read() )
    for [element_name, candidates] in data:
        files = [ f for name, f in cfg.cali_files if name==element_name ]
        if not len(files)==1:
            raise ValueError(
                    "There should be exactly ONE file for every entry in the extrema JSON (No Match for {})".format(element_name))
        opt, hist = Histogram.Read( cfg.cali_dir+files[0], files[0][:-4], files[0][:-4] )
        hist -= opt.time / opt_rausch.time * rausch

        back_edges = [ edges for t, *edges in candidates if t=="B_edge" ]
        back_edges = [ tuple(p) for sublist in back_edges for p in sublist ]
        comp_edges = [ edges for t, *edges in candidates if t=="C_edge" ]
        comp_edges = [ tuple(p) for sublist in comp_edges for p in sublist ]
        peaks = [ edges for t, *edges in candidates if t=="peak" ]
        peaks = [ tuple(p) for sublist in peaks for p in sublist ]

        back_edges_fits = edge_fit( hist, back_edges, right=False, plot=False, out=out )
        comp_edges_fits = edge_fit( hist, comp_edges, right=True, plot=False, out=out )
        peak_fits = peak_fit( hist, peaks, plot=False, out=out )

        back_pos = []
        if out:
            print("Backscatter:")
        for f in back_edges_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            back_pos.append( ( paras[2] - paras[3], np.sqrt(sig_paras[2]**2+sig_paras[3]**2) ) ) # e = a - d
            if out:
                print("\t{:.2f} +- {:.2f}".format(*back_pos[-1]))
        comp_pos = []
        if out:
            print("Compton scatter:")
        for f in comp_edges_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            comp_pos.append(( paras[2] + paras[3], np.sqrt(sig_paras[2]**2+sig_paras[3]**2) )) # e = a + d
            if out:
                print("\t{:.2f} +- {:.2f}".format(*comp_pos[-1]))
        peak_pos = []
        if out:
            print("Photopeaks:")
        for f in peak_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            peak_pos.append(( paras[3], sig_paras[3] )) # e = [3]
            if out:
                print("\t{:.2f} +- {:.2f}".format(*peak_pos[-1]))

        if plot:
            canvas = TCanvas("canvas","canvas")
            hist.Draw(xName="channel number", yName="counts")
            if element_name == "60Co":
                legend = TLegend(.14,.68,.35,.89)
            if element_name == "137Cs":
                legend = TLegend(.70,.16,.89,.37)
            if element_name == "152Eu":
                legend = TLegend(.40,.75,.60,.89)
            if element_name == "22Na":
                legend = TLegend(.70,.30,.89,.51)
                
            legend.AddEntry(hist.hist, "Data")
            i=0
            for f in back_edges_fits:
                f.function.SetLineColor(3)
                f.function.Draw("Same")
                if i == 0:
                    legend.AddEntry(f.function, "backscatter fit")
                    i = 1
            i=0
            for f in comp_edges_fits:
                f.function.SetLineColor(6)
                f.function.Draw("Same")
                if i == 0:
                    legend.AddEntry(f.function, "compton fit")
                    i = 1
            i=0
            for f in peak_fits:
                f.function.SetLineColor(2)
                f.function.Draw("Same")
                if i == 0:
                    legend.AddEntry(f.function, "peak fit")
                    i = 1
            legend.Draw()
            canvas.SaveAs( graph_dir + element_name + ".eps" )
            input()
            

def calibrate():
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "Rauschmessung" )

    for name, f in cfg.cali_files:
        opt, hist = Histogram.Read( cfg.cali_dir+f, f[:-4], f[:-4] )
        hist -= opt.time / opt_rausch.time * rausch
        
        hist.Draw()
        input()

if __name__ == "__main__":
    
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )

    calibrate_known( True, True, True )
