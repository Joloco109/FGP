import numpy as np
from ROOT import TF1, TCanvas, TLine, TLegend, gPad, TGaxis

from graph import MultiGraph
from calibration import calibrate_C, calibrate_Pt
from function import Function
from section import section
from calibration import k_boltzmann, eVolt

import os

graph_dir = "Graphs/build/"

minNLin = 36
maxNLin = 70
minLin = 150
maxSpr = 40
minRes = [ 1, 1 ]
maxRes = [ 170, 200 ]
minExt = [ 175, 200 ]
maxExt = [ 220, 255 ]

colorsCu = [ 4, 7 ]
colorsTa = [ 2, 3 ]
colorsSi = [ 6, 1 ]

def draw( graph, funcX=None, funcY=None, options=None ):
    if not funcY==None:
        graph.Apply( funcY )
    if not funcX==None:
        graph.ApplyX( funcX )
    if options==None:
        graph.Draw()
    else:
        graph.Draw( options=options )


if __name__=="__main__":
    if not os.path.exists( graph_dir ):
        os.makedirs( graph_dir )
    if not os.path.exists( graph_dir + "a/" ):
        os.makedirs( graph_dir + "a/" )
    if not os.path.exists( graph_dir + "b/" ):
        os.makedirs( graph_dir + "b/" )
    if not os.path.exists( graph_dir + "c/" ):
        os.makedirs( graph_dir + "c/" )
    if not os.path.exists( graph_dir + "e/" ):
        os.makedirs( graph_dir + "e/" )

    flog = Function( TF1("log", "log(x)" ) )
    finv_log = Function( TF1("inv log", "log(1/x)" ) )
    finv = Function( TF1("inv", "1/x" ) )
    fto_C = Function( TF1("to_C", "x-273.15" ) )

    caliC = calibrate_C()
    graphHe = MultiGraph.Read( "Data/He.txt", lambda x: caliC.GetX((x[1],0))[0], [None,None,"Cu","Ta","Si",None,None] )
    sectionHe = section(graphHe)

    caliPt = calibrate_Pt()
    graphN = MultiGraph.Read( "Data/N.txt", lambda x: caliPt.GetX((x[0],0))[0], [None,None,"Cu","Ta","Si",None,None] )
    sectionN = section(graphN)

    minT = 0.9*min( 0,
            *[ np.min(g.GetX()) for g in sectionHe.subgraphs ],
            *[ np.min(g.GetX()) for g in sectionN.subgraphs ])
    maxT = 1.1* max(
            *[ np.max(g.GetX()) for g in sectionHe.subgraphs ],
            *[ np.max(g.GetX()) for g in sectionN.subgraphs ])

    minTSi = 0.9 * min( np.min( sectionHe.subgraphs[2].GetX() ),
                np.min( sectionN.subgraphs[2].GetX() ))
    maxTSi = 1.1 * max( np.max( sectionHe.subgraphs[2].GetX() ),
                np.max( sectionN.subgraphs[2].GetX() ))


    #Sections
    #whole data
    canvas = TCanvas("canvas","canvas")

    CuHe = sectionHe.subgraphs[0]
    CuHe.graph.SetMarkerSize( 2 )
    CuHe.graph.SetMarkerColor( colorsCu[0] )
    CuHe.GetXaxis().SetLimits( minT, maxT )
    CuHe.Draw( options="AP", marker=5 )
    CuHe.graph.SetTitle("averaged and calibrated measurement (Cu + Ta)")

    TaHe = sectionHe.subgraphs[1]
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( colorsTa[0] )
    TaHe.Draw( options="P", marker=5 )

    CuN = sectionN.subgraphs[0]
    CuN.graph.SetMarkerSize( 2 )
    CuN.graph.SetMarkerColor( colorsCu[1] )
    CuN.Draw( options="P", marker=5 )

    TaN = sectionN.subgraphs[1]
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( colorsTa[1] )
    TaN.Draw( options="P", marker=5 )

    legend = TLegend(.80,.14,.89,.45)
    legend.AddEntry(CuHe.graph, "Cu He")
    legend.AddEntry(TaHe.graph, "Ta He")
    legend.AddEntry(CuN.graph, "Cu N")
    legend.AddEntry(TaN.graph, "Ta N")
    legend.Draw()

    minNLinline = TLine( minNLin, 0, minNLin, 20 )
    maxNLinline = TLine( maxNLin, 0, maxNLin, 20 )
    minLinline = TLine( minLin, 0, minLin, 20 )
    minNLinline.Draw()
    maxNLinline.Draw()
    minLinline.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "Cu_Ta.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    for i in range(2):
        print(maxRes[i])
        minResline = TLine( minRes[i], 0, minRes[i], 120e6 )
        maxResline = TLine( maxRes[i], 0, maxRes[i], 120e6 )
        minResline.SetLineColor( colorsSi[i] )
        maxResline.SetLineColor( colorsSi[i] )
        minResline.Draw()
        maxResline.Draw()
        minExtline = TLine( minExt[i], 0, minExt[i], 120e6 )
        maxExtline = TLine( maxExt[i], 0, maxExt[i], 120e6 )
        minExtline.SetLineColor( colorsSi[i] )
        maxExtline.SetLineColor( colorsSi[i] )
        minExtline.Draw()
        maxExtline.Draw()

    SiHe = sectionHe.subgraphs[2].Clone()
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( colorsSi[0])
    SiHe.GetXaxis().SetLimits( minTSi, maxTSi )
    SiHe.Draw( options="AP", marker=5 )
    SiHe.graph.SetTitle("averaged and calibrated measurement (Si)")

    SiN = sectionN.subgraphs[2].Clone()
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( colorsSi[1])
    SiN.Draw( options="P", marker=5 )

    legend = TLegend(.80,.14,.89,.30)
    legend.AddEntry(SiHe.graph, "Si He")
    legend.AddEntry(SiN.graph, "Si N")
    legend.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "Si.eps" )
    input()


    # Fits
    #   linear
    flin_CuHe = Function( TF1( "lin_CuHe", "pol1" ))
    flin_CuN  = Function( TF1( "lin_CuN", "pol1" ))
    flin_TaHe = Function( TF1( "lin_TaHe", "pol1" ))
    flin_TaN  = Function( TF1( "lin_TaN", "pol1" ))
    for f in [flin_CuHe, flin_CuN, flin_TaHe, flin_TaN]:
        f.function.SetParameter( 0, 17 )
        f.function.SetParameter( 1, 7e-2 )

    CuHe_lin = sectionHe.subgraphs[0].Slice(minLin, None).ApplyX( fto_C )
    CuN_lin = sectionN.subgraphs[0].Slice(minLin, None).ApplyX( fto_C )
    TaHe_lin = sectionHe.subgraphs[1].Slice(minLin, None).ApplyX( fto_C )
    TaN_lin = sectionN.subgraphs[1].Slice(minLin, None).ApplyX( fto_C )

    for f,g in zip( [flin_CuHe, flin_CuN, flin_TaHe, flin_TaN],
                    [CuHe_lin, CuN_lin, TaHe_lin, TaN_lin ]):
        g.Fit( f, "Q" )
        pars = f.GetParameters()
        es = f.GetParErrors()
        print( f.function )
        print( "T_0   = {:6.3f} +- {:6.3f}".format( pars[0], es[0] ) )
        alpha = pars[1]/pars[0]
        e_alpha = np.sqrt( (es[1]/pars[0])**2 + (es[0]*pars[1]/(pars[0])**2)**2 )
        print( "alpha =({:6.5f} +- {:6.5f})*10^-3".format( alpha*1e3, e_alpha*1e3 ))
        print( "Chi/N = {:6.3f}".format( f.GetChisquare()/f.GetNDF() ))
        print()

    # R over T
    canvas = TCanvas("canvas","canvas")
    CuHe_lin.graph.SetMarkerSize( 2 )
    CuHe_lin.graph.SetMarkerColor( colorsCu[0])
    CuHe_lin.GetXaxis().SetLimits( fto_C.Eval(minLin), fto_C.Eval(maxT) )
    CuHe_lin.Draw( options="AP", marker=5, xName = "T [#circ C]" )
    CuHe_lin.graph.SetTitle("linear regime Cu")
    CuN_lin.graph.SetMarkerSize( 2 )
    CuN_lin.graph.SetMarkerColor( colorsCu[1] )
    CuN_lin.Draw( options="P", marker=5 )

    legendCu_lin = TLegend(.70,.14,.89,.30)
    legendCu_lin.AddEntry(CuHe_lin.graph, "Cu He")
    legendCu_lin.AddEntry(CuN_lin.graph, "Cu N")
    legendCu_lin.AddEntry(flin_CuN.function, "R = R_0(1+\\alpha T)")
    legendCu_lin.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "c/Cu_lin.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe_lin.graph.SetMarkerSize( 2 )
    TaHe_lin.graph.SetMarkerColor( colorsTa[0])
    TaHe_lin.GetXaxis().SetLimits( fto_C.Eval(minLin), fto_C.Eval(maxT) )
    TaHe_lin.Draw( options="AP", marker=5, xName = "T [#circ C]" )
    TaHe_lin.graph.SetTitle("linear regime Ta")
    TaN_lin.graph.SetMarkerSize( 2 )
    TaN_lin.graph.SetMarkerColor( colorsTa[1] )
    TaN_lin.Draw( options="P", marker=5 )

    legendTa_lin = TLegend(.70,.14,.89,.30)
    legendTa_lin.AddEntry(TaHe_lin.graph, "Ta He")
    legendTa_lin.AddEntry(TaN_lin.graph, "Ta N")
    legendTa_lin.AddEntry(flin_TaN.function, "R = R_0(1+\\alpha T)")
    legendTa_lin.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "c/Ta_lin.eps" )
    input()

    #   non-linear
    f_CuHe = Function( TF1( "CuHe", "[0] + [1]*x^[2]" ))
    f_TaHe = Function( TF1( "TaHe", "[0] + [1]*x^[2]" ))
    for f in [f_CuHe, f_TaHe ]:
        f.function.SetParameter( 0, 0.1 )
        f.function.SetParameter( 1, 0.001e-6 )
        f.function.SetParLimits( 1, 0.0005e-6, 0.004e-6 )
        f.function.SetParameter( 2, 5.0 )
        f.function.SetParLimits( 2, 4.5, 5.5 )

    CuHe = sectionHe.subgraphs[0].Slice(minNLin,maxNLin)
    CuN = sectionN.subgraphs[0].Slice(minNLin,maxNLin)
    TaHe = sectionHe.subgraphs[1].Slice(minNLin,maxNLin)
    TaN = sectionN.subgraphs[1].Slice(minNLin,maxNLin)

    for f,g in zip( [f_CuHe, f_TaHe ],
                    [CuHe, TaHe ]):
        g.Fit( f, "Q" )
        pars = f.GetParameters()
        es = f.GetParErrors()
        print( f.function )
        print( "T_0 = {:6.5f} +- {:6.5f}".format( pars[0], es[0] ) )
        print( "A   =({:6.5f} +- {:6.5f})*10^-6".format( pars[1]*1e6, es[1]*1e6 ) )
        print( "beta= {:6.5f} +- {:6.5f}".format( pars[2], es[2] ) )
        print( "Chi/N = {:6.3f}".format( f.GetChisquare()/f.GetNDF() ))
        print()

    # R over T
    canvas = TCanvas("canvas","canvas")
    CuHe.graph.SetMarkerSize( 2 )
    CuHe.graph.SetMarkerColor( colorsCu[0])
    CuHe.Draw( options="AP", marker=5 )
    CuHe.graph.SetTitle("non-linear regime Cu")
    CuN.graph.SetMarkerSize( 2 )
    CuN.graph.SetMarkerColor( colorsCu[1] )
    CuN.Draw( options="P", marker=5 )

    legendCu = TLegend(.34,.79,.66,.92)
    legendCu.AddEntry(CuHe.graph, "Cu He")
    legendCu.AddEntry(f_CuHe.function, "R = R_0+A T^\\beta")
    legendCu.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "a/Cu.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( colorsTa[0])
    TaHe.Draw( options="AP", marker=5 )
    TaHe.graph.SetTitle("non-linear regime Ta")
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( colorsTa[1] )
    TaN.Draw( options="P", marker=5 )

    legendTa = TLegend(.34,.79,.66,.92)
    legendTa.AddEntry(TaHe.graph, "Ta He")
    legendTa.AddEntry(f_TaHe.function, "R = R_0+A T^\\beta")
    legendTa.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "a/Ta.eps" )
    input()

    # ln(R) over ln(T)
    f_CuHelog = Function( TF1( "CuHe", "log([0] + [1]*e^(x*[2]))", 3.5, 4.5 ))
    f_TaHelog = Function( TF1( "TaHe", "log([0] + [1]*e^(x*[2]))", 3.5, 4.5 ))
    for f_log, f in zip( [f_CuHelog, f_TaHelog ], [f_CuHe, f_TaHe ] ):
        p = f.GetParameters()
        for i in range(len(p)):
            f_log.function.SetParameter( i, p[i] )

    canvas = TCanvas("canvas","canvas")
    CuHe.ApplyX( flog ).Apply( flog )
    CuN.ApplyX( flog ).Apply( flog )
    CuHe.Draw( options="AP", marker=5, xName= "ln(T) [K]", yName= "ln(R) [\\Omega]")
    CuHe.graph.SetTitle("log scale non-linear regime Cu")
    CuN.Draw( options="P", marker=5 )
    f_CuHelog.function.Draw( "LSame" )

    legendCu = TLegend(.26,.78,.74,.93)
    legendCu.AddEntry(CuHe.graph, "Cu He")
    legendCu.AddEntry(f_CuHelog.function, "R = R_0 + A T^\\beta")
    legendCu.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "a/ln_Cu.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe.ApplyX( flog ).Apply( flog )
    TaN.ApplyX( flog ).Apply( flog )
    TaHe.Draw( options="AP", marker=5, xName= "ln(T) [K]", yName= "ln(R) [\\Omega]" )
    TaHe.graph.SetTitle("log scale non-linear regime Ta")
    TaN.Draw( options="P", marker=5 )
    f_TaHelog.function.Draw( "LSame" )

    legendTa = TLegend(.26,.78,.74,.93)
    legendTa.AddEntry(TaHe.graph, "Ta He")
    legendTa.AddEntry(f_TaHelog.function, "R = R_0 + A T^\\beta")
    legendTa.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "a/ln_Ta.eps" )
    input()

    # Sprung
    TaHe_spr = sectionHe.subgraphs[1].Slice(None,maxSpr)
    T = TaHe_spr.GetX()
    Tc_min = max( [ t for t in T if t < 20] )
    Tc_max = min( [ t for t in T if t > 20] )
    Tc = (Tc_max+Tc_min)/2
    err_Tc = (Tc_max-Tc_min)/np.sqrt(12)
    print( "Tc = {:6.5f} +- {:6.5f}".format( Tc, err_Tc ))
    Tcline = TLine( Tc, 0, Tc, 0.15 )
    Tc_minline = TLine( Tc_min, 0, Tc_min, 0.15 )
    Tc_maxline = TLine( Tc_max, 0, Tc_max, 0.15 )

    canvas = TCanvas("canvas","canvas")
    TaHe_spr.graph.SetMarkerSize( 2 )
    TaHe_spr.graph.SetMarkerColor( colorsTa[0] )
    TaHe_spr.Draw( options="AP", marker=5 )
    Tcline.Draw()
    Tc_minline.Draw()
    Tc_maxline.Draw()
    canvas.Update()
    canvas.SaveAs( graph_dir + "e/Sprung.eps" )
    input()


    # ln 1/R over 1/T
    fres_SiHe = Function( TF1( "res_SiHe", "pol1", 1/maxRes[0], 1/minRes[0] ))
    fres_SiN  = Function( TF1( "res_SiN", "pol1", 1/maxRes[1], 1/minRes[1] ))
    for f in [fres_SiHe, fres_SiN ]:
        f.function.SetParameter( 0, 0 )
        f.function.SetParameter( 1, -6e2 )

    SiHe_res = sectionHe.subgraphs[2].Clone().Apply( finv_log ).ApplyX( finv )
    SiN_res = sectionN.subgraphs[2].Clone().Apply( finv_log ).ApplyX( finv )

    for f,g in zip( [ fres_SiHe, fres_SiN ],
                    [ SiHe_res, SiN_res ] ) :
        g.Fit( f, "RQ" )
        pars = f.GetParameters()
        es = f.GetParErrors()
        print( f.function )
        print( "A     = {:6.3f} +- {:6.3f}".format( pars[0], es[0] ) )
        print( "delta = {:6.5f} +- {:6.5f}".format( pars[1], es[1] ))
        print( "Chi/N = {:6.3f}".format( f.GetChisquare()/f.GetNDF() ))
        energy_d = -2*k_boltzmann / eVolt * pars[1]
        sig_ed = -2*k_boltzmann / eVolt * es[1]
        print( "E_d   =({:6.5f} +- {:6.5f})eV".format( energy_d, sig_ed ))
        print()

    canvas = TCanvas("canvas","canvas")
    #minResLine = TLine( 1/minRes, -18, 1/minRes, -12 )
    #maxResLine = TLine( 1/maxRes, -18, 1/maxRes, -12 )
    #minResLine.Draw()
    #maxResLine.Draw()

    SiHe_res.graph.SetMarkerSize( 2 )
    SiHe_res.graph.SetMarkerColor( colorsSi[0] )
    SiHe_res.GetXaxis().SetLimits( finv.Eval(maxTSi), finv.Eval(minTSi) )
    SiHe_res.Draw( options="AP", marker=5, xName= "1/T [1/K]", yName= "ln(1/R[K])" )
    SiHe_res.graph.SetTitle("Fit on freeze out regime of Si")
    SiN_res.graph.SetMarkerSize( 2 )
    SiN_res.graph.SetMarkerColor( colorsSi[1] )
    SiN_res.Draw( options="P", marker=5 )

    legendSi_inv = TLegend(.26,.78,.74,.93)
    legendSi_inv.AddEntry(SiHe_res.graph, "Si He")
    legendSi_inv.AddEntry(SiN_res.graph, "Si N")
    legendSi_inv.AddEntry(fres_SiHe.function, "1/R = A exp( \\delta/T )")
    legendSi_inv.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "b/Si_Tinv.eps" )
    input()

    # ln 1/R over ln T
    fext_SiHe = Function( TF1( "ext_SiHe", "pol1", np.log(minExt[0]), np.log(maxExt[0]) ))
    fext_SiN  = Function( TF1( "ext_SiN", "pol1", np.log(minExt[1]), np.log(maxExt[1]) ))
    for f in [fext_SiHe, fext_SiN ]:
        f.function.SetParameter( 0, 0 )
        f.function.SetParameter( 1, -6e2 )

    SiHe_ext = sectionHe.subgraphs[2].Clone().Apply( finv_log ).ApplyX( flog )
    SiN_ext = sectionN.subgraphs[2].Clone().Apply( finv_log ).ApplyX( flog )

    for f,g in zip( [ fext_SiHe, fext_SiN ],
                    [ SiHe_ext, SiN_ext ] ) :
        g.Fit( f, "RQ" )
        pars = f.GetParameters()
        es = f.GetParErrors()
        print( f.function )
        print( "ln(A) = {:6.3f} +- {:6.3f}".format( pars[0], es[0] ) )
        print( "A     = {:6.3e} +- {:6.3e}".format( np.exp(pars[0]), np.exp(pars[0])*es[0] ) )
        print( "gamma = {:6.5f} +- {:6.5f}".format( pars[1], es[1] ))
        if f.GetNDF() == 0:
            print("Chi = {:4.2f}".format(f.GetChisquare()))
            print("You overfitted with laughable few data points!\nWhat did you expect?")
        else:
            print("Chi/Ndf = {:4.2f}".format(f.GetChisquare()/f.GetNDF()))
        print()

    canvas = TCanvas("canvas","canvas")
    #minResLine = TLine( np.log(minExt), -18, np.log(minExt), -13 )
    #maxResLine = TLine( np.log(maxExt), -18, np.log(maxExt), -13 )
    #minResLine.Draw()
    #maxResLine.Draw()

    SiHe_ext.graph.SetMarkerSize( 2 )
    SiHe_ext.graph.SetMarkerColor( colorsSi[0] )
    SiHe_ext.GetXaxis().SetLimits( flog.Eval(minTSi), flog.Eval(maxTSi) )
    SiHe_ext.Draw( options="AP", marker=5, xName= "ln(T[K])", yName= "ln(1/R[\\Omega])" )
    SiHe_ext.graph.SetTitle("Fit on extrinsic regime of Si")
    SiN_ext.graph.SetMarkerSize( 2 )
    SiN_ext.graph.SetMarkerColor( colorsSi[1] )
    SiN_ext.Draw( options="P", marker=5 )

    legendSi_ext = TLegend(.30,.78,.70,.93)
    legendSi_ext.AddEntry(SiHe_ext.graph, "Si He")
    legendSi_ext.AddEntry(SiN_ext.graph, "Si N")
    legendSi_ext.AddEntry(fext_SiN.function, "1/R = A T^\\gamma")
    legendSi_ext.Draw()

    canvas.Update()
    canvas.SaveAs( graph_dir + "b/Si_doubleLog.eps" )
    input()
