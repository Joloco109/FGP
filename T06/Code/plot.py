from reader import Hist
from ROOT import TCanvas

def plot_hist( hist, logy=False ):
    canvas = TCanvas('hist_canvas', 'Histogram', 200, 10, 700, 500)
    if logy :
        canvas.SetLogy()
    hist.hist.Draw("E1")
    canvas.Update()
    input()

def plot_graph( graph, logy=False ):
    canvas = TCanvas('graph_canvas', 'Graph', 200, 10, 700, 500)
    if logy :
        canvas.SetLogy()
    graph.graph.SetMarkerColor(4)
    graph.graph.SetMarkerSize(5)
    graph.graph.Draw("ap")
    canvas.Update()
    input()
