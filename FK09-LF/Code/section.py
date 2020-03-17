import numpy as np

from calibration import calibrate_C, calibrate_Pt
from graph import Graph, MultiGraph

def section( graph, tresh=0.07 ):
    T = np.array(graph.GetX(0))
    vals = np.array(graph.GetY())
    new_vals = []
    start = None
    for i in range(1,len(T)):
        if start == None:
            start = i-1
            continue
        if np.abs(1-T[i]/np.mean(T[start:i])) > tresh :
            if i+1<len(T) and np.abs( np.mean(T[start:i])-T[i] ) < np.abs( T[i]-T[i+1] ):
                continue
            new_vals.append( (
                    (np.mean( T[start:i] ), np.std( T[start:i] )),
                    *[ (np.mean( v[start:i] ), np.std( v[start:i] )) for v in vals]
                ) )
            start = None
    else :
        new_vals.append( (
                (np.mean( T[start:len(T)] ), np.std( T[start:len(T)] )),
                *[ (np.mean( v[start:len(T)] ), np.std( v[start:len(T)] )) for v in vals]
            ) )

    ret_graph = MultiGraph()
    tem = np.array( [row[0][0] for row in new_vals] )
    err_tem = np.array( [row[0][1] for row in new_vals] )
    for i in range(len(graph.subgraphs)):
        name = graph.subgraphs[i].name
        res = np.array( [row[i+1][0] for row in new_vals] )
        err_res = np.array( [row[i+1][1] for row in new_vals] )

        ret_graph.Add(
                Graph( name, tem, res, err_tem, err_res ) )
    return ret_graph


def main():
    print()
    caliC = calibrate_C()
    graphHe = MultiGraph.Read( "Data/He.txt", lambda x: caliC.GetX((x[1],0))[0], [None,None,"Cu","Ta","Si",None,None] )
    sectionHe = section( graphHe, 0.005 )
    for g, s in zip( graphHe.subgraphs, sectionHe.subgraphs ):
        g.graph.SetMarkerColor(4)
        g.Draw( options="A*" )
        s.Draw( options="P" )
        input()

    caliPt = calibrate_Pt()
    graphN = MultiGraph.Read( "Data/N.txt", lambda x: caliPt.GetX((x[0],0))[0], [None,None,"Cu","Ta","Si",None,None] )
    sectionN = section( graphN, 0.005 )
    for g, s in zip( graphN.subgraphs, sectionN.subgraphs ):
        g.graph.SetMarkerColor(4)
        g.Draw( options="A*" )
        s.Draw( options="P" )
        input()

if __name__=="__main__":
    main()
