import codecs
import numpy as np
from ROOT import TGraph, TGraphErrors, TF1

from function import Function

class Graph:
    def __init__( self, name, x, y, ex=None, ey=None, esx=None, esy=None ):
        self.name = name
        if not (type(None)==type(ex) and type(None)==type(ey)):
            if type(None) == type(ex):
                ex = np.zeros(len(x))
            if type(None) == type(ey):
                ey = np.zeros(len(y))

            data = np.array([ d for d in zip(x,y,ex,ey) if not (d[0]==None or d[1]==None) ])
            self.graph=TGraphErrors( len(data) )

            for i in range(len(data)):
                self.graph.SetPointError( i, data[i][2], data[i][3] )

        else :
            data = np.array([ d for d in zip(x,y) if not (d[0]==None or d[1]==None) ])
            self.graph = TGraph( len(data) )

        self.graph.SetTitle( name )
        for i in range(len(data)):
            self.graph.SetPoint( i, data[i][0], data[i][1] )

        if type(None) == type(esx):
            esx = np.zeros(len(x))
        if type(None) == type(esy):
            esy = np.zeros(len(y))
        self.syserrorsX2 = esx**2
        self.syserrorsY2 = esy**2

    def Clone( self ):
        c = Graph( self.name, [], [])
        c.graph = self.graph.Clone()
        c.syserrorsX2 = self.syserrorsX2.copy()
        c.syserrorsY2 = self.syserrorsY2.copy()
        return c

    def Slice( self, start, end ):
        x = self.GetX()
        if not start == None:
            i, = np.where( start <= x )
        else :
            i = np.array([ range(len(x)) ])
        if not end== None:
            j, = np.where( x < end )
        else:
            j = np.array([ range(len(x)) ])
        i = np.intersect1d( i, j )
        x = np.take( x, i )
        y = np.take( self.GetY(), i )
        try:
            ex = np.take( self.GetEX(), i )
            ey = np.take( self.GetEY(), i )
        except ValueError:
            ex = None
            ey = None
        esx = np.take( self.GetEXSys(), i )
        esy = np.take( self.GetEYSys(), i )
        return Graph( self.name, x, y, ex, ey, esx, esy )

    def ApplyY( self, func ):
        x = self.GetX()
        ex = self.GetEX()
        y = self.GetY()
        ey = self.GetEY()
        for i in range(len(y)):
            new_y = func.Get(( y[i], ey[i] ))
            self.graph.SetPoint( i, x[i], new_y[0] )
            self.graph.SetPointError( i, ex[i], new_y[1] )

            new_y = func.Get(( y[i], np.sqrt(self.syserrorsY2[i]) ))
            self.syserrorsY2[i] = new_y[2]**2 + self.syserrorsY2[i]
        return self

    def ApplyX( self, func ):
        x = self.GetX()
        ex = self.GetEX()
        y = self.GetY()
        ey = self.GetEY()
        for i in range(len(x)):
            new_x = func.Get(( x[i], ex[i] ))
            self.graph.SetPoint( i, new_x[0], y[i] )
            self.graph.SetPointError( i, new_x[1], ey[i] )

            new_x = func.Get(( x[i], np.sqrt(self.syserrorsX2[i]) ))
            self.syserrorsX2[i] = new_x[2]**2 + self.syserrorsX2[i]
        return self

    def Scale( self, s ):
        scaler = Function( TF1("scale_{}".format(s), "[0]*x" ) )
        scaler.function.SetParameter( 0, s )
        self.Apply( scaler )
        self.syserrorsX2 *= s**2
        self.syserrorsY2 *= s**2
        return self

    def Fit( self, function, options="", plot=True, out=True ):
        if not plot:
            options = "N" + options
        if not out:
            options = "Q" + options
        return self.graph.Fit( function.function, options )

    def Draw( self, options="AP", marker=6, xName = "", yName = "" ):
        self.graph.SetLineWidth(1)
        self.graph.SetMarkerStyle(marker)
        self.GetXaxis().SetTitle( xName )
        self.GetYaxis().SetTitle( yName ) 
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

    def GetEXSys( self ):
        return np.sqrt( self.syserrorsX2 )

    def GetEYSys( self ):
        return np.sqrt( self.syserrorsY2 )

    def GetXaxis( self ):
        return self.graph.GetXaxis()

    def GetYaxis( self ):
        return self.graph.GetYaxis()
