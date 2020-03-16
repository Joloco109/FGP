import codecs
import numpy as np
from ROOT import TGraph, TMultiGraph

class MultiGraph :
    def Read( file_name, x_axis, y_names ):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = np.array([ [ float(x) for x in row.strip().replace(",",".").split() ] for row in content if not row.strip()=="" ])
        x = np.array([ x_axis(row) for row in content ])
        content = content.T

        if not len(content) == len(y_names):
            raise ValueError("len(content) = {} is not equal to len(y_names)={}".format(len(content),len(y_names)))

        subgraphs = []
        multigraph = TMultiGraph()
        for y, name in zip(content, y_names):
            if not name == None:
                graph = Graph( x, y, name )
                subgraphs.append( graph )
                multigraph.Add( graph.graph, name )

        graph = MultiGraph()
        graph.subgraphs = subgraphs
        graph.multigraph = multigraph
        return graph

    def Draw( self, i=None, options="AP", marker=6 ):
        if i==None:
            self.multigraph.SetLineWidth(4)
            self.multigraph.SetMarkerStyle(marker)
            self.multigraph.Draw(options)
        else:
            self.subgraphs[i].Draw( options=options, marker=marker )

    def GetX( self, i ):
        return self.subgraphs[i].GetX()

    def GetY( self, i ):
        return self.subgraphs[i].GetY()

    def GetEX( self, i ):
        return self.subgraphs[i].GetEX()

    def GetEY( self, i ):
        return self.subgraphs[i].GetEY()

class Graph:
    def __init__( self, x, y, name ):
        self.name = name
        self.graph = TGraph( len(x) )
        for i in range(len(x)):
            self.graph.SetPoint( i, x[i], y[i] )

    def Draw( self, options="AP", marker=6 ):
        self.graph.SetLineWidth(4)
        self.graph.SetMarkerStyle(marker)
        self.graph.Draw(options)

    def ArrayFromPointer( self, pointer ):
        return np.array( np.fromiter(
            pointer,
            dtype=np.float64,
            count=self.graph.GetN()
            ) )

    def GetX( self ):
        return self.ArrayFromPointer( self.graph.GetX() )

    def GetY( self ):
        return self.ArrayFromPointer( self.graph.GetY() )

    def GetEX( self ):
        return self.ArrayFromPointer( self.graph.GetEX() )

    def GetEY( self ):
        return self.ArrayFromPointer( self.graph.GetEY() )
