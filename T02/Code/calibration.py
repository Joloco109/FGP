from ROOT import TF1, TCanvas, TLegend
import numpy as np

from function import Function

class Calibration(Function):
    def __init__( self, graph, function ):
        self.graph = graph
        if type( function ) == Function:
            self.function = function.function
        else :
            self.function = function

    def Draw( self ):
        self.graph.Draw()

    def GetXaxis( self ):
        return self.graph.GetXaxis()

    def GetYaxis( self ):
        return self.graph.GetYaxis()
