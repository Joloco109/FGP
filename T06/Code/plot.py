from reader import Hist
from ROOT import TCanvas

def plot_hist( hist, logy=False ):
    canvas = TCanvas('canvas', 'Histogram', 200, 10, 700, 500)
    if logy :
        canvas.SetLogy()
    hist.hist.Draw()
    canvas.Update()
    input()
