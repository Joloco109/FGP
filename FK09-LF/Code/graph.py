import codecs
import numpy as np
from ROOT import TGraph, TGraphErrors, TMultiGraph

class MultiGraph :
    def Read( file_name, x_axis, y_names ):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = np.array([ [ float(x) if float(x) < 989999999999999934e20 else None
            for x in row.strip().replace(",",".").split() ] for row in content if not row.strip()=="" ])
        x = np.array([ x_axis(row) for row in content ])
        content = content.T

        if not len(content) == len(y_names):
            raise ValueError("len(content) = {} is not equal to len(y_names)={}".format(len(content),len(y_names)))

        subgraphs = []
        multigraph = TMultiGraph()
        for y, name in zip(content, y_names):
            if not name == None:
                graph = Graph( name, x, y )
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
    def __init__( self, name, x, y, ex=None, ey=None ):
        self.name = name
        if not (type(None)==type(ex) and type(None)==type(ey)):
            self.graph=TGraphErrors( len(x) )
            if type(None) == type(ex):
                ex = np.zeros(len(x))
            if type(None) == type(ey):
                ey = np.zeros(len(y))
            for i in range(len(x)):
                if x[i]==None or y[i]==None:
                    continue
                self.graph.SetPointError( i, ex[i], ey[i] )

        else :
            self.graph = TGraph( len(x) )

        self.graph.SetTitle( name )
        for i in range(len(x)):
            if x[i]==None or y[i]==None:
                continue
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
        if not type(self.graph)==TGraphErrors:
            raise ValueError("GetEX cant be called on Graph of type {}".format(type(self.graph)))
        return self.ArrayFromPointer( self.graph.GetEX() )

    def GetEY( self ):
        if not type(self.graph)==TGraphErrors:
            raise ValueError("GetEY cant be called on Graph of type {}".format(type(self.graph)))
        return self.ArrayFromPointer( self.graph.GetEY() )

    def GetXaxis( self ):
        return self.graph.GetXaxis()

    def GetYaxis( self ):
        return self.graph.GetYaxis()
