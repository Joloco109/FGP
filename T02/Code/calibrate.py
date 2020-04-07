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

m_e = 511 # electron mass [keV]
sig_me = 1

graph_dir = "Graphs/build/calibrate/"

def back_edge( e, sig_e ):
    return ( e/(1 + 2*e/m_e), np.abs(1/(1+2*e/m_e)**2)*sig_e, np.abs(1/(1+m_e/(2*e))**2)*sig_me )

def comp_edge( e, sig_e ):
    return ( e/(1 + m_e/(2*e)), np.abs(1-1/(1+2*e/m_e)**2)*sig_e, np.abs(1/(1+m_e/(2*e))**2)*sig_me )

def analyse_element( element_name, candidates, rausch, cali=None, out=False ):
        (opt_rausch, rausch) = rausch
        files = [ f for name, f in cfg.cali_files if name==element_name ]
        if not len(files)==1:
            raise ValueError(
                    "There should be exactly ONE file for every entry in the extrema JSON (No Match for {})".format(element_name))

        opt, hist = Histogram.Read( cfg.cali_dir+files[0], files[0][:-4], files[0][:-4], calibration=cali )
        hist -= opt.time / opt_rausch.time * rausch

        back_edges = [ edges for t, *edges in candidates if t=="B_edge" ]
        comp_edges = [ edges for t, *edges in candidates if t=="C_edge" ]
        peaks = [ edges for t, *edges in candidates if t=="peak" ]
        if cali==None:
            back_edges = [ tuple(p) for sublist in back_edges for p in sublist ]
            comp_edges = [ tuple(p) for sublist in comp_edges for p in sublist ]
            peaks = [ tuple(p) for sublist in peaks for p in sublist ]
        else:
            back_edges = [ tuple( [cali.Get((x,0))[0] for x in p ] )
                    for sublist in back_edges for p in sublist ]
            comp_edges = [ tuple( [cali.Get((x,0))[0] for x in p ] )
                    for sublist in comp_edges for p in sublist ]
            peaks = [ tuple( [cali.Get((x,0))[0] for x in p ] )
                    for sublist in peaks for p in sublist ]

        back_edges_fits = edge_fit( hist, back_edges, right=False, plot=False, out=out )
        comp_edges_fits = edge_fit( hist, comp_edges, right=True, plot=False, out=out )
        peak_fits = peak_fit( hist, peaks, plot=False, out=out )

        back_pos = []
        if out:
            print("Backscatter:")
        for f in back_edges_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            back_pos.append( ( paras[2] - paras[3], np.sqrt(sig_paras[2]**2+sig_paras[3]**2+paras[4]**2) ) ) # e = a - d
            if out:
                print("\t{:.2f} \\pm {:.2f}".format(*back_pos[-1]))
        comp_pos = []
        if out:
            print("Compton scatter:")
        for f in comp_edges_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            comp_pos.append(( paras[2] + paras[3], np.sqrt(sig_paras[2]**2+sig_paras[3]**2+paras[4]**2) )) # e = a + d
            if out:
                print("\t{:.2f} \\pm {:.2f}".format(*comp_pos[-1]))
        peak_pos = []
        if out:
            print("Photopeaks:")
        for f in peak_fits:
            paras = f.GetParameters()
            sig_paras = f.GetParErrors()
            peak_pos.append(( paras[3], np.sqrt(sig_paras[3]**2+paras[4]**2) )) # e = [3]
            if out:
                print("\t{:.2f} \\pm {:.2f}".format(*peak_pos[-1]))
        return hist, (back_edges_fits, back_pos), (comp_edges_fits, comp_pos), (peak_fits, peak_pos)

def plot_element( element_name, hist, back_edges_fits, comp_edges_fits, peak_fits, xName="", yName="", save=False, graph_dir="" ):
    canvas = TCanvas("canvas","canvas")
    hist.Draw(xName=xName, yName=yName)
    if element_name == "60Co":
        legend = TLegend(.14,.68,.35,.89)
    if element_name == "137Cs":
        legend = TLegend(.70,.16,.89,.37)
    if element_name == "152Eu":
        legend = TLegend(.40,.75,.60,.89)
    if element_name == "22Na":
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
        canvas.SaveAs( graph_dir + element_name + ".eps" )
    input()

def calibrate_known( plot=False, out=False, save=False ):
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "noise measurement" )
    if plot:
        canvas = TCanvas("canvas","canvas")
        rausch.Draw(xName="channel number", yName="counts")
        if save:
            canvas.SaveAs( graph_dir + "noise.eps" )
        input()

    data = json.loads( open( cfg.cali_dir+cfg.cali_extrema ).read() )
    known_energies = json.loads( open( cfg.cali_dir+cfg.cali_energy_extrema ).read() )

    data_points = [[], []]
    data_type = []

    for [element_name, candidates] in data:
        (
            hist,
            (back_edges_fits, back_pos),
            (comp_edges_fits, comp_pos),
            (peak_fits, peak_pos)
        ) = analyse_element( element_name, candidates, (opt_rausch, rausch), out=out )

        es = [ e for name, e in known_energies if name==element_name ]
        if len(es)>1:
            raise ValueError(
                    "There should be at maximum ONE entry for every entry in the extrema JSON (No Match for {})".format(element_name))
        if len(es) > 0:
            back_es = [ None if e==None else back_edge(*e)
                    for t, *b_es in es[0] if t == "B_edge"  for e in b_es ]

            comp_es = [ None if e==None else comp_edge(*e)
                    for t, *c_es in es[0] if t == "C_edge"  for e in c_es ]

            peak_es = [ None if e==None else tuple([*e,0])
                    for t, *p_es in es[0] if t == "peak" for e in p_es ]

            if back_es == []:
                back_pos = []
            if comp_es == []:
                comp_pos = []
            if peak_es == []:
                peak_pos = []

            if out:
                print("Mapping: pos energy")
                
            data_type.extend([(element_name,"back") for i in back_es if not i == None])
            data_type.extend([(element_name,"comp") for i in comp_es if not i == None])
            data_type.extend([(element_name,"peak") for i in peak_es if not i == None])
            
            for pos, e in zip(back_pos+comp_pos+peak_pos, back_es+comp_es+peak_es):
                if not e == None:
                    if out:
                        print( "\t",pos[0], e[0] )
                    data_points[0].append([pos[0],pos[1]])
                    data_points[1].append([e[0],e[1]])

            if out:
                print()

        if plot:
            plot_element( element_name, hist, back_edges_fits, comp_edges_fits, peak_fits,
                    xName="channel number", yName="counts", save=save, graph_dir=graph_dir )

    positions = np.array(data_points[0])
    energies = np.array(data_points[1])

    cali_graph = Graph( "Calibration", positions[:,0], energies[:,0], positions[:,1], energies[:,1] )
    cali = Function( TF1( "Calibration", "pol1" ) )
    cali_graph.Fit( cali, plot=plot, out=out )
    cali = Calibration( cali_graph, cali )

    if out:
        print("Calibration:")
        print("\tE_lost = {:.5f} \\pm {:.5f}".format(-cali.GetParameters()[0], cali.GetParErrors()[0]))
        print("\tk      = {:.5f} \\pm {:.5f}".format(cali.GetParameters()[1], cali.GetParErrors()[1]))
        print("\tChi^2/NdF = {:.3f}".format(cali.GetChisquare()/cali.GetNDF()))

    if plot:
        canvas = TCanvas("canvas","canvas")
        legend = TLegend(.14,.60,.35,.89)
        cali_graph.Draw(xName = "channel number", yName = "Energy [keV]")
        legend.AddEntry(cali.function, "E = K\\cdot x - E_{lost}")
        markers = []

        for p,e,(n,t) in zip(positions[:,0],energies[:,0], data_type):
                m = TMarker(p, e, cfg.cali_marker[t])
                m.SetMarkerSize(2)
                m.SetMarkerColor(cfg.cali_marker[n])
                m.Draw()
                markers.append(m)
        leg_markers = []

        for name, _ in known_energies:
                m = TMarker(-100, -100, 21)
                m.SetMarkerColor(cfg.cali_marker[name])
                legend.AddEntry(m, name)
                leg_markers.append(m)
        i = 0
        for key in cfg.cali_marker:
            if i < len(cfg.cali_files):
                i+=1
            else:
                m = TMarker(-100, -100, cfg.cali_marker[key])
                m.SetMarkerColor(1)
                legend.AddEntry(m, key)
                leg_markers.append(m)
        legend.Draw()
        if save:
            canvas.SaveAs( graph_dir + "calibration_lin_reg.eps" )
        input()

    return cali


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
