import numpy as np
import os
from ROOT import TCanvas,TLegend, TF1, TMarker

from calibration import Calibration
from histogram import Histogram
from graph import Graph
import config as cfg
from finder import find_edges, peak_fit, edge_fit

graph_dir = "Graphs/build/efficiency/" 

def efficiency( plot=False, out=False, save=False ):
    opt_noise, noise = Histogram.Read( cfg.eff_dir+cfg.eff_files[0], "noise", "noise measurement" )
    if plot:
        canvas = TCanvas("canvas","canvas")
        noise.Draw(xName="channel number", yName="counts")
        if save:
            canvas.SaveAs( graph_dir + "noise.eps" )
        input()
    opt, hist = Histogram.Read( cfg.eff_dir+cfg.eff_files[1], "eff", "efficiency measurement" )
    hist -= opt.time / opt_noise.time * noise
    if plot:
        canvas = TCanvas("canvas","canvas")
        hist.Draw(xName="channel number", yName="counts")
        if save:
            canvas.SaveAs( graph_dir + "efficency.eps" )
        input()
if __name__ == "__main__":
    
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )

    efficiency( True, True, True )