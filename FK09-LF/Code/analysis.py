from ROOT import TF1, TCanvas

from graph import MultiGraph
from calibration import calibrate_C, calibrate_Pt
from function import Function
from section import section

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
    for g in sectionHe.subgraphs[:2]:
        draw( g, None, None  )
        input()
    '''

    cloneHe = sectionHe.Clone()
    for g in cloneHe.subgraphs[:2]:
        draw( g, flog, None  )
        input()
    cloneHe = sectionHe.Clone()
    for g in cloneHe.subgraphs[:2]:
        draw( g, flog, flog )
        input()
    '''


    caliPt = calibrate_Pt()
    graphN = MultiGraph.Read( "Data/N.txt", lambda x: caliPt.GetX((x[0],0))[0], [None,None,"Cu","Ta","Si",None,None] )
    sectionN = section(graphN)
    for g in sectionN.subgraphs[:2]:
        draw( g, None, None  )
        input()
    '''

    cloneN = sectionN.Clone()
    for g in cloneN.subgraphs[:2]:
        draw( g, flog, None  )
        input()
    cloneN = sectionN.Clone()
    for g in cloneN.subgraphs[:2]:
        draw( g, flog, flog )
        input()
    '''

    canvas = TCanvas("canvas","canvas")
    for gHe, gN in zip( sectionHe.subgraphs, sectionN.subgraphs):
        gHe.graph.SetMarkerColor(4)
        gN.graph.SetMarkerColor(6)
        gHe.Draw( options="AP" )
        gN.Draw( options="P" )
        input()
