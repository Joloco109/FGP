import numpy as np
import os
from ROOT import TCanvas,TLegend, TF1, TMarker

from calibration import Calibration
from histogram import Histogram
from graph import Graph
import config as cfg
from finder import find_edges, peak_fit, edge_fit

graph_dir = "Graphs/build/efficiency/" 
peak_area = [(380, 480)]
element_name = "137Cs"

def efficiency( plot=False, out=False, save=False ):
    opt_noise, noise = Histogram.Read( cfg.eff_dir+cfg.eff_files[0], "noise", "noise measurement" )
   
    opt, hist = Histogram.Read( cfg.eff_dir+cfg.eff_files[1], "eff", "efficiency measurement" )
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
        hist.Draw(xName="channel number", yName="counts")
        n = hist.hist.Integral(380, 480)
        print("Root: ", n)
        for f in peak_fits:
            f.function.SetLineColor(2)
            f.function.Draw("Same")
        input()
        N = paras[2]*paras[4]*np.sqrt(2*np.pi)
        N_err = np.sqrt((paras[4]*np.sqrt(2*np.pi)*sig_paras[2])**2+(paras[2]*np.sqrt(2*np.pi)*sig_paras[4])**2)
        print("Analytic: ", N ," \pm ", N_err)
        
    if save:
        canvas.SaveAs( graph_dir + "efficency.eps" ) 
        
if __name__ == "__main__":
    
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )
    efficiency( True, True, True)