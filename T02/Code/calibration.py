from ROOT import TF1, TCanvas, TLegend
import numpy as np

from function import Function

class Calibration(Function):
    def __init__( self, graph, function, parSysError=None ):
        self.graph = graph
        if type( function ) == Function:
            function = function.function
        super( Calibration, self).__init__( function, parSysError )

    def Draw( self ):
        self.graph.Draw()

    def GetXaxis( self ):
        return self.graph.GetXaxis()

    def GetYaxis( self ):
        return self.graph.GetYaxis()
