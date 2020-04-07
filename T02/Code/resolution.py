import numpy as np
import json
import os
from ROOT import TCanvas, TLine, TLegend, TF1

from histogram import Histogram
from graph import Graph
from function import Function
from calibrate import analyse_element, calibrate_known, plot_element
import config as cfg

graph_dir = "Graphs/build/resolution/"

def resolution( plot=False, out=False, save=False ):
    cali = calibrate_known()

    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch,
            "Rauschmessung", "noise measurement", calibration=cali )

    data = json.loads( open( cfg.cali_dir+cfg.cali_extrema ).read() )
    known_energies = json.loads( open( cfg.cali_dir+cfg.cali_energy_extrema ).read() )

    data_points = []

    for [element_name, candidates] in data:
        (
            hist,
            (back_edges_fits, back_pos),
            (comp_edges_fits, comp_pos),
            (peak_fits, peak_pos)
        ) = analyse_element( element_name, candidates, (opt_rausch, rausch), cali=cali, out=out )

        if out:
            print(element_name+":")
            print("\t Position       <=> Resolution")
        #for f, pos in zip( back_edges_fits+comp_edges_fits+peak_fits, back_pos+comp_pos+peak_pos ):
        for f, pos in zip( peak_fits, peak_pos ):
            pars = f.GetParameters()
            sig_pars = f.GetParErrors()
            if out:
                print("\t {: >6.1f} \\pm {: >4.1f} &  {: >4.1f} \\pm {: >4.1f}".format( pos[0], pos[1], pars[4], sig_pars[4] ))

            data_points.append( [*pos, pars[4], sig_pars[4] ] )
        
        if plot:
            plot_element( element_name, hist, back_edges_fits, comp_edges_fits, peak_fits,
                    xName="Energy[keV]", yName="Count", save=save, graph_dir=graph_dir )

    for i, d in zip(range(len(data_points)), data_points ):
        if d[2] > 35:
            print(i, d)
    del data_points[14]
    data_points = np.array(data_points)
    e = data_points[:,0]
    sig_e = data_points[:,1]
    res = data_points[:,2]
    sig_res = data_points[:,3]

    res_graph = Graph( "Resolution", e, res, sig_e, sig_res )
    res_fun = Function( TF1( "Resolution", "x*sqrt([0]**2+[1]**2/x)" ) )
    res_fun.function.SetParameter(0, 2e-3 )
    res_fun.function.SetParameter(1, 5e-1 )
    res_graph.Fit( res_fun, plot=plot, out=out )
    pars = res_fun.GetParameters()
    sig_pars = res_fun.GetParErrors()

    if out:
        print("Resolution:")
        print("\ta = {:.5f} \\pm {:.5f}".format(pars[0], sig_pars[0]))
        print("\tb = {:.5f} \\pm {:.5f}".format(pars[1], sig_pars[1]))
        print("\tChi^2/NdF = {:.3f}".format(res_fun.GetChisquare()/res_fun.GetNDF()))

    if plot:
        canvas = TCanvas("canvas","canvas")
        legend = TLegend(.14,.84,.55,.89)
        res_graph.Draw(xName = "E[keV]", yName = r"\sigma_E[keV]")
        legend.AddEntry(res_fun.function, r"\sigma_E/E = \sqrt{a^2+b^2/E}")
        legend.Draw()
        if save:
            canvas.SaveAs(graph_dir+"resolution.eps")
        input()

    return res_fun

if __name__=="__main__":
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )

    res = resolution( True, True, True )
