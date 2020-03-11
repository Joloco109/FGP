from ROOT import TGraphErrors, TF1

class Graph:
    def __init__( self, x, y ):
        if len(x) != len(y):
            raise ValueError
        self.graph = TGraphErrors( len(x) )
        for i in range(len(x)):
            self.graph.SetPoint( i, x[i][0], y[i][0] )
            self.graph.SetPointError( i, x[i][1], y[i][1] )

    def fit( self, title, func ):
        fit = TF1( title, func )
        self.graph.Fit( fit )
        return fit
