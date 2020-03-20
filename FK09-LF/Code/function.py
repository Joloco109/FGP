import numpy as np

class Function:
    def __init__( self, function ):
        self.function = function

    def Get( self, x ):
        return (
                self.function.Eval( x[0] ),
                np.abs(self.function.Derivative( x[0] )) * x[1]
                )

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
