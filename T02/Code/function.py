from ctypes import pointer, c_float
import numpy as np

class Function:
    def __init__( self, function, parSysError=None ):
        self.function = function
        if type(None) == type(parSysError):
            parSysError = np.zeros(function.GetNpar())
        self.syserrorsP2 = parSysError**2

    def Clone( self ):
        f = Function( self.function.Clone(), parSysError=self.syserrorsP2.copy() )
        return f

    def Get( self, x ):
        return (
                self.function.Eval( x[0] ),
                np.abs(self.function.Derivative( x[0] )) * x[1],
                np.sqrt( sum([ self.function.GradientPar( i, pointer(c_float(x[0])) )**2 * (ep**2 + eps**2)
                    for i, ep, eps in zip(range(self.function.GetNpar()), self.GetParErrors(), self.GetParErrorsSys()) ]) )
                )

    def Eval( self, x ):
        return self.function.Eval( x )

    def GetX( self, y ):
        x = self.function.GetX( y[0], 0, 1e5 )
        return ( x,
                y[1] / np.abs(self.function.Derivative( x ))
                )

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

    def GetParErrorsSys( self ):
        return np.sqrt( self.syserrorsP2 )

    def SetParErrorsSys( self, syserrorsP ):
        self.syserrorsP2 = syserrorsP**2
        return self
