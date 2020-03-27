from ROOT import TF1, TCanvas, TLegend
import numpy as np

from function import Function

class Calibration(Function):
    def __init__( self, graph, function ):
        self.graph = graph
        self.function = function

    def Draw( self ):
        self.graph.Draw()

    def GetNDF( self ):
        return self.function.GetNDF()

    def GetChisquare( self ):
        return self.function.GetChisquare()

    def ArrayFromPointer( self, pointer ):
        return np.array( np.fromiter(
            pointer,
            dtype=np.float64,
            count=self.function.GetNpar()
            ) )

    def GetParameters( self ):
        return self.ArrayFromPointer( self.function.GetParameters() )

    def GetParErrors( self ):
        return self.ArrayFromPointer( self.function.GetParErrors() )

    def GetXaxis( self ):
        return self.graph.GetXaxis()

    def GetYaxis( self ):
        return self.graph.GetYaxis()
