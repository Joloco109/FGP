from ROOT import TF1
import numpy as np

class Calibration:
    def __init__( self, function ):
        self.function = function

    def get( self, x ):
        return (
                self.function.Eval( x[0] ),
                np.abs(self.function.Derivative( x[0] )) * x[1],
                0
                #np.sqrt( sum( [
                    #( self.function.GradientPar(i, x[0]) * self.function.GetParError(i) )**2
                    #for i in range( self.function.GetNpar() )]))
                )
