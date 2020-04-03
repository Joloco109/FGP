import json

from calibration import Calibration
from histogram import Histogram
import config as cfg
from finder import find_edges, peak_fit, edge_fit

def calibrate_known():
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "Rauschmessung" )

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

        back_edges_fits = edge_fit( hist, back_edges, right=False )
        comp_edges_fits = edge_fit( hist, comp_edges, right=True )
        peak_fits = peak_fit( hist, peaks )

        hist.Draw()
        input()
        hist.Draw()
        for f in back_edges_fits:
            f.function.Draw("Same")
        for f in comp_edges_fits:
            f.function.Draw("Same")
        for f in peak_fits:
            f.function.Draw("Same")
        input()

def calibrate():
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "Rauschmessung" )

    for name, f in cfg.cali_files:
        opt, hist = Histogram.Read( cfg.cali_dir+f, f[:-4], f[:-4] )
        hist -= opt.time / opt_rausch.time * rausch

        hist.Draw()
        input()

if __name__ == "__main__":
    calibrate_known()
