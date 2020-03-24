import numpy as np
from ROOT import TF1, TCanvas, TLine, TLegend

from graph import MultiGraph
from calibration import calibrate_C, calibrate_Pt
from function import Function
from section import section

graph_dir = "Graphs/"

minT = 20
maxT = 70
minLin = 150
maxSpr = 40
minExt = 0
maxExt = 377

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


    #Sections
    canvas = TCanvas("canvas","canvas")

    CuHe = sectionHe.subgraphs[0]
    CuHe.graph.SetMarkerSize( 2 )
    CuHe.graph.SetMarkerColor( 4 )
    CuHe.Draw( options="AP", marker=5 )
    CuHe.graph.SetTitle("helium measurement")
    
    TaHe = sectionHe.subgraphs[1]
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( 2 )
    TaHe.Draw( options="P", marker=5 )

    SiHe = sectionHe.subgraphs[2]
    rightmax = 1.1*np.max(SiHe.GetY())
    scale = max( np.max(CuHe.GetY()), np.max(TaHe.GetY()) ) / rightmax
    SiHe.Scale( scale )
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 6 )
    SiHe.Draw( options="P", marker=5 )
    
    legendHe = TLegend(.40,.77,.60,.92)
    legendHe.AddEntry(CuHe.graph, "Cu")
    legendHe.AddEntry(TaHe.graph, "Ta")
    legendHe.AddEntry(SiHe.graph, "Si")
    legendHe.Draw()
    
    minTline = TLine( minT, 0, minT, 20 )
    maxTline = TLine( maxT, 0, maxT, 20 )
    minLinline = TLine( minLin, 0, minLin, 20 )
    minTline.Draw()
    maxTline.Draw()
    minLinline.Draw()
    canvas.SaveAs( graph_dir + "Helium.eps" )
    input()


    canvas = TCanvas("canvas","canvas")
    CuN = sectionN.subgraphs[0]
    CuN.graph.SetMarkerSize( 2 )
    CuN.graph.SetMarkerColor( 4 )
    CuN.Draw( options="AP", marker=5 )
    CuN.graph.SetTitle("nitrogen measurement")
    
    TaN = sectionN.subgraphs[1]
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( 2 )
    TaN.Draw( options="P", marker=5 )

    SiN = sectionN.subgraphs[2]
    SiN.Scale( scale )
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 6 )
    SiN.Draw( options="P", marker=5 )

    legendN = TLegend(.40,.77,.60,.92)
    legendN.AddEntry(CuHe.graph, "Cu")
    legendN.AddEntry(TaHe.graph, "Ta")
    legendN.AddEntry(SiHe.graph, "Si")
    legendN.Draw()

    minTline = TLine( minT, 0, minT, 20 )
    maxTline = TLine( maxT, 0, maxT, 20 )
    minLinline = TLine( minLin, 0, minLin, 20 )
    minTline.Draw()
    maxTline.Draw()
    minLinline.Draw()
    canvas.SaveAs( graph_dir + "Nitrogen.eps" )
    input()
    
    #whole data
    canvas = TCanvas("canvas","canvas")
    CuN = sectionN.subgraphs[0]
    CuN.graph.SetMarkerSize( 2 )
    CuN.graph.SetMarkerColor( 7 )
    CuN.Draw( options="AP", marker=5 )
    CuN.graph.SetTitle("averaged and calibrated measurement")
    
    TaN = sectionN.subgraphs[1]
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( 3 )
    TaN.Draw( options="P", marker=5 )

    SiN = sectionN.subgraphs[2]
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 1 )
    SiN.Draw( options="P", marker=5 )

    CuHe = sectionHe.subgraphs[0]
    CuHe.graph.SetMarkerSize( 2 )
    CuHe.graph.SetMarkerColor( 4 )
    CuHe.Draw( options="P", marker=5 )
    
    TaHe = sectionHe.subgraphs[1]
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( 2 )
    TaHe.Draw( options="P", marker=5 )

    SiHe = sectionHe.subgraphs[2]
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 6 )
    SiHe.Draw( options="P", marker=5 )
    
    legend = TLegend(.80,.14,.89,.45)
    legend.AddEntry(CuHe.graph, "Cu He")
    legend.AddEntry(TaHe.graph, "Ta He")
    legend.AddEntry(SiHe.graph, "Si He")
    legend.AddEntry(CuN.graph, "Cu N")
    legend.AddEntry(TaN.graph, "Ta N")
    legend.AddEntry(SiN.graph, "Si N")
    legend.Draw()

    minTline = TLine( minT, 0, minT, 20 )
    maxTline = TLine( maxT, 0, maxT, 20 )
    minLinline = TLine( minLin, 0, minLin, 20 )
    minTline.Draw()
    maxTline.Draw()
    minLinline.Draw()
    
    canvas.SaveAs( graph_dir + "Data.eps" )
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
        print( "alpha =({:6.5f} +- {:6.5f})*10^3".format( alpha*1e3, e_alpha*1e3 ))
        print( "Chi/N = {:6.3f}".format( f.GetChisquare()/f.GetNDF() ))
        print()

    # R over T
    canvas = TCanvas("canvas","canvas")
    CuHe_lin.graph.SetMarkerSize( 2 )
    CuHe_lin.graph.SetMarkerColor( 6 )
    CuHe_lin.Draw( options="AP", marker=5, xName = "T [#circ C]" )
    CuHe_lin.graph.SetTitle("linear regime Cu")
    CuN_lin.graph.SetMarkerSize( 2 )
    CuN_lin.graph.SetMarkerColor( 4 )
    CuN_lin.Draw( options="P", marker=5 )
    
    legendCu_lin = TLegend(.40,.77,.60,.92)
    legendCu_lin.AddEntry(CuHe_lin.graph, "Cu He")
    legendCu_lin.AddEntry(CuN_lin.graph, "Cu N")
    legendCu_lin.AddEntry(flin_CuN.function, "R = R_0(1+\\alpha T)")
    legendCu_lin.Draw()
    
    canvas.SaveAs( graph_dir + "c/Cu_lin.eps" )
    input()
    
    canvas = TCanvas("canvas","canvas")
    TaHe_lin.graph.SetMarkerSize( 2 )
    TaHe_lin.graph.SetMarkerColor( 6 )
    TaHe_lin.Draw( options="AP", marker=5, xName = "T [#circ C]" )
    TaHe_lin.graph.SetTitle("linear regime Ta")
    TaN_lin.graph.SetMarkerSize( 2 )
    TaN_lin.graph.SetMarkerColor( 4 )
    TaN_lin.Draw( options="P", marker=5 )
    
    legendTa_lin = TLegend(.40,.77,.60,.92)
    legendTa_lin.AddEntry(TaHe_lin.graph, "Ta He")
    legendTa_lin.AddEntry(TaN_lin.graph, "Ta N")
    legendTa_lin.AddEntry(flin_TaN.function, "R = R_0(1+\\alpha T)")
    legendTa_lin.Draw()
    
    canvas.SaveAs( graph_dir + "c/Ta_lin.eps" )
    input()

    #   non-linear
    f_CuHe = Function( TF1( "CuHe", "[0] + [1]*x^[2]" ))
    f_TaHe = Function( TF1( "TaHe", "[0] + [1]*x^[2]" ))
    for f in [f_CuHe, f_TaHe ]:
        f.function.SetParameter( 0, 1e-3 )
        f.function.SetParameter( 1, 6.6e-6 )
        f.function.SetParameter( 2, 3 )
        f.function.SetParLimits( 2, 1, 10 )

    CuHe = sectionHe.subgraphs[0].Slice(minT,maxT)
    CuN = sectionN.subgraphs[0].Slice(minT,maxT)
    TaHe = sectionHe.subgraphs[1].Slice(minT,maxT)
    TaN = sectionN.subgraphs[1].Slice(minT,maxT)

    for f,g in zip( [f_CuHe, f_TaHe ],
                    [CuHe, TaHe ]):
        g.Fit( f, "Q" )
        pars = f.GetParameters()
        es = f.GetParErrors()
        print( f.function )
        print( "T_0 = {:6.3f} +- {:6.3f}".format( pars[0], es[0] ) )
        print( "A   =({:6.5f} +- {:6.5f})*10^-6".format( pars[1]*1e6, es[1]*1e6 ) )
        print( "beta= {:6.5f} +- {:6.5f}".format( pars[2], es[2] ) )
        print( "Chi/N = {:6.3f}".format( f.GetChisquare()/f.GetNDF() ))
        print()

    # R over T
    canvas = TCanvas("canvas","canvas")
    CuHe.graph.SetMarkerSize( 2 )
    CuHe.graph.SetMarkerColor( 6 )
    CuHe.Draw( options="AP", marker=5 )
    CuHe.graph.SetTitle("non-linear regime Cu")
    CuN.graph.SetMarkerSize( 2 )
    CuN.graph.SetMarkerColor( 4 )
    CuN.Draw( options="P", marker=5 )
    
    legendCu = TLegend(.40,.77,.60,.92)
    legendCu.AddEntry(CuHe.graph, "Cu He")
    legendCu.AddEntry(CuN.graph, "Cu N")
    legendCu.AddEntry(f_CuHe.function, "R = R_0+A\\cdot T^\\beta")
    legendCu.Draw()
    
    canvas.SaveAs( graph_dir + "a/Cu.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( 6 )
    TaHe.Draw( options="AP", marker=5 )
    TaHe.graph.SetTitle("non-linear regime Ta")
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( 4 )
    TaN.Draw( options="P", marker=5 )
    
    legendTa = TLegend(.40,.77,.60,.92)
    legendTa.AddEntry(TaHe.graph, "Ta He")
    legendTa.AddEntry(TaN.graph, "Ta N")
    legendTa.AddEntry(f_TaHe.function, "R = R_0+A\\cdot T^\\beta")
    legendTa.Draw()
    
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
    
    legendCu = TLegend(.28,.76,.72,.93)
    legendCu.AddEntry(CuHe.graph, "Cu He")
    legendCu.AddEntry(CuN.graph, "Cu N")
    legendCu.AddEntry(f_CuHelog.function, "ln(R) = ln(R_0 + A e^{T \\cdot \\beta })")
    legendCu.Draw()
    
    canvas.SaveAs( graph_dir + "a/ln_Cu.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe.ApplyX( flog ).Apply( flog )
    TaN.ApplyX( flog ).Apply( flog )
    TaHe.Draw( options="AP", marker=5, xName= "ln(T) [K]", yName= "ln(R) [\\Omega]" )
    TaHe.graph.SetTitle("log scale non-linear regime Ta")
    TaN.Draw( options="P", marker=5 )
    f_TaHelog.function.Draw( "LSame" )
    
    legendTa = TLegend(.28,.76,.72,.93)
    legendTa.AddEntry(TaHe.graph, "Ta He")
    legendTa.AddEntry(TaN.graph, "Ta N")
    legendTa.AddEntry(f_TaHelog.function, "ln(R) = ln(R_0 + A e^{T \\cdot \\beta })")
    legendTa.Draw()
    
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
    TaHe_spr.graph.SetMarkerColor( 2 )
    TaHe_spr.Draw( options="AP", marker=5 )
    Tcline.Draw()
    Tc_minline.Draw()
    Tc_maxline.Draw()
    canvas.SaveAs( graph_dir + "a/Ta.eps" )
    input()


    # ln 1/R over 1/T
    canvas = TCanvas("canvas","canvas")
    SiHe = sectionHe.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( finv )
    SiN = sectionN.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( finv )
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 2 )
    SiHe.Draw( options="AP", marker=5, xName= "ln(1/T) [1/K]", yName= "ln(1/R) [1/\\Omega]" )
    SiHe.graph.SetTitle("inverse log scale Si")
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 4 )
    SiN.Draw( options="P", marker=5 )
    
    legendSi_inv = TLegend(.40,.77,.60,.92)
    legendSi_inv.AddEntry(SiHe.graph, "Si He")
    legendSi_inv.AddEntry(SiN.graph, "Si N")
    legendSi_inv.Draw()
    
    canvas.SaveAs( graph_dir + "b/Si_inv.eps" )
    input()

    # ln 1/R over ln T
    canvas = TCanvas("canvas","canvas")
    SiHe = sectionHe.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( flog )
    SiN = sectionN.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( flog )
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 2 )
    SiHe.Draw( options="AP", marker=5, xName= "ln(T) [K]", yName= "ln(1/R) [1/\\Omega]" )
    SiHe.graph.SetTitle("Mobility in Si ")
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 4 )
    SiN.Draw( options="P", marker=5 )
    
    legendSi = TLegend(.40,.77,.60,.92)
    legendSi.AddEntry(SiHe.graph, "Si He")
    legendSi.AddEntry(SiN.graph, "Si N")
    legendSi.Draw()
    
    canvas.SaveAs( graph_dir + "b/Si.eps" )
    input()
