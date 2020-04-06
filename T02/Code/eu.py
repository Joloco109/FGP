import json
import numpy as np
from ROOT import TCanvas, TLegend, TLine

import config as cfg
from histogram import Histogram
from calibrate import calibrate_known, analyse_element
from energies import Element

cali = calibrate_known()
rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "noise measurement", cali )
data = json.loads( open( cfg.cali_dir+cfg.cali_extrema ).read() )

(
        hist,
        (back_edges_fits, back_pos),
        (comp_edges_fits, comp_pos),
        (peak_fits, peak_pos)
    ) = analyse_element(  data[2][0], data[2][1], rausch, cali, True, True )

canvas = TCanvas("canvas","canvas")
hist.Draw(xName="Energy [keV]", yName="counts")
legend = TLegend(.40,.75,.60,.89)
    
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

amplitudes = []
i=0
for f in peak_fits:
    f.function.SetLineColor(2)
    f.function.Draw("Same")
    if i == 0:
        legend.AddEntry(f.function, "peak fit")
        i = 1
    pars = f.GetParameters()
    sig_pars = f.GetParErrors()
    N = np.sqrt(2*np.pi) * pars[4] * pars[2]
    amplitudes.append( ((pars[3], sig_pars[3]), N ) )
legend.Draw()

scale = np.max(hist.GetBinContents())/np.max(np.array(amplitudes)[:,1])
peaks = []
for e, a in amplitudes:
    p = TLine( e[0], 0, e[0], a*scale )
    p.SetLineColor(2)
    p.SetLineWidth(2)
    peaks.append(p)

products = Element.Read( cfg.cali_dir+"energies_eu.json" )[0].products
gamma_peaks = []
scale *= np.sum(np.array(amplitudes)[:,1])/np.sum(products['gamma'][2])
for e, sig_e, i in products['gamma'].T:
    p = TLine( e, 0, e, i*scale)
    p.SetLineColor(41)
    p.SetLineWidth(4)
    gamma_peaks.append(p)

null = TLine( 0, 0, np.max(hist.GetBinLowEdges()), 0 )
null.Draw()
for p in gamma_peaks+peaks:
    p.Draw()
legend.AddEntry(gamma_peaks[0], "Literature Gamma decays")
canvas.Update()

for e, a in amplitudes:
    i_min = np.argmin( np.abs(products['gamma'][0] - e[0]) )
    e_min, sig_e, i = products['gamma'][:,i_min]
    print("Closest decay to Peak at E=({:.4f} \\\\pm {:.4f})keV:".format( *e ))
    print("\t({:.4f} \\\\pm {:.4f})keV".format( e_min, sig_e ))

input()
