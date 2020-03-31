import codecs
import numpy as np
import numbers
from ROOT import TH1I, TF1

from function import Function

class DataOptions:
    def __init__( self, time ):
        self.time = time

class Histogram:
    def __init__( self, name, title=None, bins=None, calibration=None ):
        if title==None:
            title = name
            
        self.name = name
        self.title = title

        self.cali = calibration

        if not bins == None:
            if calibration==None:
                self.hist = TH1I( self.name, self.title, len(bins), 0, len(bins) )
            else:
                self.hist = TH1I( self.name, self.title, len(bins), calibration.Eval(0), calibration.Eval(len(bins)) )

            for i in range(len(bins)):
                self.hist.SetBinContent( i+1, bins[i] )
            self.hist.Sumw2()
        else:
            self.hist = None
            

    def Read( file_name, name, title ):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = [ x.strip() for x in content]
        time = float(content[0])
        data = [ int(x) for x in content[1:] if not x=='' ]

        return DataOptions( time ), Histogram( name, title, data )

    def Clone( self ):
        h = Histogram( self.name, self.title, None, self.cali )
        h.hist = self.hist.Clone()
        return h

    def Fit( self, function, options=None ):
        if options==None:
            return self.hist.Fit( function.function )
        else:
            return self.hist.Fit( function.function, options )

    def Draw( self, options="", marker=5, xName = "", yName = "" ):
        if not xName=="":
            self.GetXaxis().SetTitle( xName )
        if not yName=="":
            self.GetYaxis().SetTitle( yName ) 
        self.hist.Draw(options)
        
    def GetBinCenters( self ):
        return np.array([ self.hist.GetBinCenter(i+1) for i in range(self.GetNcells()) ])

    def GetBinCenterErrors( self ):
        return np.array([ self.hist.GetBinWidth(i+1) for i in range(self.GetNcells()) ])/np.sqrt(12)

    def GetBinContents( self ):
        return np.array([ self.hist.GetBinContent(i+1) for i in range(self.GetNcells()) ])

    def GetBinErrors( self ):
        return np.array([ self.hist.GetBinError(i+1) for i in range(self.GetNcells()) ])

    def GetEY( self ):
        if not type(self.graph)==TGraphErrors:
            raise ValueError("GetEY cant be called on Graph of type {}".format(type(self.graph)))
        return self.ArrayFromPointer( self.graph.GetEY() )

    def GetXaxis( self ):
        return self.hist.GetXaxis()

    def GetYaxis( self ):
        return self.hist.GetYaxis()

    def Add( self, rhs ):
        if isinstance( rhs, Histogram ):
            self.hist.Add( rhs.hist )
        elif isinstance( rhs, Function ):
            self.hist.Add( rhs.function )
        else:
            raise TypeError
        return self

    def Multiply( self, rhs ):
        if isinstance( rhs, Histogram ):
            self.hist.Multiply( rhs.hist )
        elif isinstance( rhs, Function ):
            self.hist.Multiply( rhs.function )
        elif isinstance( rhs, numbers.Number ):
            self.hist.Scale( rhs )
        else:
            raise TypeError
        return self

    def Divide( self, rhs ):
        if isinstance( rhs, Histogram ):
            self.hist.Divide( rhs.hist )
        elif isinstance( rhs, Function ):
            self.hist.Divide( rhs.function )
        elif isinstance( rhs, numbers.Number ):
            self.hist.Scale( 1/rhs )
        else:
            raise TypeError
        return self

    def __neg__( self ):
        return self.Clone() * -1

    def __add__( self, rhs ):
        return self.Clone().Add( rhs )

    __radd__ = __add__

    def __sub__( self, rhs ):
        return self.Clone().Add( -rhs )

    def __rsub__( self, rhs ):
        return -( self - rhs )

    def __mul__( self, rhs ):
        return self.Clone().Multiply( rhs )

    __rmul__ = __mul__

    def __truediv__( self, rhs ):
        return self.Clone().Divide( rhs )

    def __iadd__( self, rhs ):
        return self.Add( rhs )

    def __isub__( self, rhs ):
        return self.Add( -rhs )

    def __imul__( self, rhs ):
        return self.Multiply( rhs )

    def __itruediv__( self, rhs ):
        return self.Divide( rhs )
