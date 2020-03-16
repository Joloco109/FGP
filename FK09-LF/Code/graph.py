import codecs
import numpy as np
from ROOT import TGraph, TMultiGraph

class MultiGraph :
    def Read( file_name, x_axis, y_names ):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = np.array([ [ float(x) for x in row.strip().replace(",",".").split() ] for row in content ])
        x = np.array([ x_axis(row) for row in content ])
        content = content.T

        if not len(content) == len(y_names):
            raise ValueError

        subgraphs = []
        multigraph = TMultiGraph()
        for y, name in zip(content, y_names):
            if not name == None:
                graph = TGraph( len(x) )
                for i in range(len(x)):
                    graph.SetPoint( i, x[i], y[i] )
                subgraphs.append( graph )
                multigraph.Add( graph, name )

        graph = MultiGraph()
        graph.subgraphs = subgraphs
        graph.multigraph = multigraph
        return graph

    def Draw( self, i=None, options="AP", marker=6 ):
        if i==None:
            to_draw = self.multigraph
        else:
            to_draw = self.subgraphs[i]

        to_draw.SetLineWidth(4)
        to_draw.SetMarkerStyle(marker)
        to_draw.Draw(options)

    def ArrayFromPointer( self, i, pointer ):
        return np.array( np.fromiter(
            pointer,
            dtype=np.float64,
            count=( self.subgraphs[i]).GetN())
            )

    def GetX( self, i ):
        return self.ArrayFromPointer( i, (
            self.subgraphs[i]
            ).GetX() )

    def GetY( self, i ):
        return self.ArrayFromPointer( i, (
            self.subgraphs[i]
            ).GetY() )

    def GetEX( self, i ):
        return self.ArrayFromPointer( i, (
            self.subgraphs[i]
            ).GetEX() )

    def GetEY( self, i ):
        return self.ArrayFromPointer( i, (
            self.subgraphs[i]
            ).GetEY() )
