import numpy as np
from ROOT import TF1, TCanvas, TLine

from graph import MultiGraph
from calibration import calibrate_C, calibrate_Pt
from function import Function
from section import section

graph_dir = "Graphs/"

minT = 20
maxT = 77
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
    minTline.Draw()
    maxTline.Draw()
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
    minTline.Draw()
    maxTline.Draw()
    canvas.SaveAs( graph_dir + "Nitrogen.eps" )
    input()

    # R over T
    canvas = TCanvas("canvas","canvas")
    CuHe = sectionHe.subgraphs[0].Slice(minT,maxT)
    CuN = sectionN.subgraphs[0].Slice(minT,maxT)
    CuHe.graph.SetMarkerSize( 2 )
    CuHe.graph.SetMarkerColor( 2 )
    CuHe.Draw( options="AP", marker=5 )
    CuN.graph.SetMarkerSize( 2 )
    CuN.graph.SetMarkerColor( 4 )
    CuN.Draw( options="P", marker=5 )
    canvas.SaveAs( graph_dir + "a/Cu.eps" )
    input()

    canvas = TCanvas("canvas","canvas")
    TaHe = sectionHe.subgraphs[1].Slice(minT,maxT)
    TaN = sectionN.subgraphs[1].Slice(minT,maxT)
    TaHe.graph.SetMarkerSize( 2 )
    TaHe.graph.SetMarkerColor( 2 )
    TaHe.Draw( options="AP", marker=5 )
    TaN.graph.SetMarkerSize( 2 )
    TaN.graph.SetMarkerColor( 4 )
    TaN.Draw( options="P", marker=5 )
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
