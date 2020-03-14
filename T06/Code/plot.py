from reader import Hist
from ROOT import TCanvas

def plot_hist( hist, logy=False, xName= "Energie/eV", save=False, directory="Spektren/"  ):
    canvas = TCanvas('hist_canvas', 'Histogram', 200, 10, 700, 500)
    hist.hist.GetXaxis().SetTitle(xName)
    if logy :
        canvas.SetLogy()
    hist.hist.Draw("E1")
    canvas.Update()
    if save:
        canvas.SaveAs(directory+hist.name()+".eps")
    input()

def plot_graph( graph, logy=False, xName="Energie/eV", yName="Energie/eV", save=False, directory="Graphen/" ):
    canvas = TCanvas('graph_canvas', 'Graph', 200, 10, 700, 500)
    graph.graph.GetXaxis().SetTitle(xName)
    graph.graph.GetYaxis().SetTitle(yName)
    if logy :
        canvas.SetLogy()
    graph.graph.SetMarkerColor(4)
    graph.graph.SetMarkerSize(5)
    graph.graph.Draw("ap")
    canvas.Update()
    if save:
        canvas.SaveAs(directory+graph.graph.GetName()+".eps")
    input()
