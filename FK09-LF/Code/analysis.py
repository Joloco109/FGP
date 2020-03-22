import numpy as np
from ROOT import TF1, TCanvas, TLine

from graph import MultiGraph
from calibration import calibrate_C, calibrate_Pt
from function import Function
from section import section

graph_dir = "Graphs/"

minT = 20
maxT = 77
minLin = 150
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

    TaHe = sectionHe.subgraphs[1]
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( 2 )
    TaHe.Draw( options="P", marker=5 )

    SiHe = sectionHe.subgraphs[2]
    rightmax = 1.1*np.max(SiHe.GetY())
    scale = max( np.max(CuHe.GetY()), np.max(TaHe.GetY()) ) / rightmax
    SiHe.Scale( scale )
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 5 )
    SiHe.Draw( options="P", marker=5 )

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

    TaN = sectionN.subgraphs[1]
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( 2 )
    TaN.Draw( options="P", marker=5 )

    SiN = sectionN.subgraphs[2]
    SiN.Scale( scale )
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 5 )
    SiN.Draw( options="P", marker=5 )

    minTline = TLine( minT, 0, minT, 20 )
    maxTline = TLine( maxT, 0, maxT, 20 )
    minLinline = TLine( minLin, 0, minLin, 20 )
    minTline.Draw()
    maxTline.Draw()
    minLinline.Draw()
    canvas.SaveAs( graph_dir + "Nitrogen.eps" )
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
    CuHe_lin.graph.SetMarkerColor( 2 )
    CuHe_lin.Draw( options="AP", marker=5 )
    CuN_lin.graph.SetMarkerSize( 2 )
    CuN_lin.graph.SetMarkerColor( 4 )
    CuN_lin.Draw( options="P", marker=5 )
    canvas.SaveAs( graph_dir + "c/Cu_lin.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe_lin.graph.SetMarkerSize( 2 )
    TaHe_lin.graph.SetMarkerColor( 2 )
    TaHe_lin.Draw( options="AP", marker=5 )
    TaN_lin.graph.SetMarkerSize( 2 )
    TaN_lin.graph.SetMarkerColor( 4 )
    TaN_lin.Draw( options="P", marker=5 )
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
    TaHe = sectionHe.subgraphs[1].Slice(minT,maxT)

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
    CuHe.graph.SetMarkerColor( 2 )
    CuHe.Draw( options="AP", marker=5 )
    canvas.SaveAs( graph_dir + "a/Cu.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( 2 )
    TaHe.Draw( options="AP", marker=5 )
    canvas.SaveAs( graph_dir + "a/Ta.eps" )
    input()

    # ln(R) over ln(T)
    canvas = TCanvas("canvas","canvas")
    CuHe.ApplyX( flog ).Apply( flog )
    CuN.ApplyX( flog ).Apply( flog )
    CuHe.Draw( options="AP", marker=5 )
    CuN.Draw( options="P", marker=5 )
    canvas.SaveAs( graph_dir + "a/ln_Cu.eps" )
    input()

    #canvas3 = TCanvas("canvas3","canvas3")
    canvas = TCanvas("canvas","canvas")
    TaHe.Apply( flog )
    TaN.Apply( flog )
    TaHe.Draw( options="AP", marker=5 )
    TaN.Draw( options="P", marker=5 )
    canvas.SaveAs( graph_dir + "a/ln_Ta.eps" )
    input()

    # ln 1/R over ln 1/T
    canvas = TCanvas("canvas","canvas")
    SiHe = sectionHe.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( finv_log )
    SiN = sectionN.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( finv_log )
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 2 )
    SiHe.Draw( options="AP", marker=5 )
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 4 )
    SiN.Draw( options="P", marker=5 )
    canvas.SaveAs( graph_dir + "b/Si_inv.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    SiHe = sectionHe.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( flog )
    SiN = sectionN.subgraphs[2].Slice(minExt,maxExt).Apply( finv_log ).ApplyX( flog )
    SiHe.graph.SetMarkerSize( 2 )
    SiHe.graph.SetMarkerColor( 2 )
    SiHe.Draw( options="AP", marker=5 )
    SiN.graph.SetMarkerSize( 2 )
    SiN.graph.SetMarkerColor( 4 )
    SiN.Draw( options="P", marker=5 )
    canvas.SaveAs( graph_dir + "b/Si.eps" )
    input()
