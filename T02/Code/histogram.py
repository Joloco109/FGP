import codecs
import numpy as np
import numbers
from ROOT import TH1F, TF1

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
                self.hist = TH1F( self.name, self.title, len(bins), 0, len(bins) )
            else:
                self.hist = TH1F( self.name, self.title, len(bins), calibration.Eval(0), calibration.Eval(len(bins)) )

            for i in range(len(bins)):
                self.hist.SetBinContent( i+1, bins[i] )
            self.hist.Sumw2()
        else:
            self.hist = None
            

    def Read( file_name, name, title, calibration=None ):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = [ x.strip() for x in content]
        time = float(content[0])
        data = [ int(x) for x in content[1:] if not x=='' ]

        return DataOptions( time ), Histogram( name, title, data, calibration=calibration )

    def Clone( self ):
        h = Histogram( self.name, self.title, None, self.cali )
        h.hist = self.hist.Clone()
        return h

    def Slice( self, start, end ):
        lows = self.GetBinLowEdges()
        if not start == None:
            i = np.where( start <= lows )[0][0]
        else :
            i = 0
        if not end== None:
            j = np.where( end <= lows )[0][0]
        else:
            j = len(lows)

        low = lows[i]
        high = lows[j]
        lows = np.take( lows, range(i,j) )
        content = np.take( self.GetBinContents(), range(i,j) )
        ec = np.take( self.GetBinErrors(), range(i,j) )

        hist = self.Clone()
        hist.hist.SetBins( int(j-i), low, high )
        for k in range(int(j-i)):
            hist.hist.SetBinContent( k+1, content[k] )
            hist.hist.SetBinError( k+1, ec[k] )
        return hist

    def Fit( self, function, options="", plot=True, out=True ):
        if not plot:
            options = "N" + options
        if not out:
            options = "Q" + options
        return self.hist.Fit( function.function, options )

    def Draw( self, options="", marker=5, xName = "", yName = "" ):
        if not xName=="":
            self.GetXaxis().SetTitle( xName )
        if not yName=="":
            self.GetYaxis().SetTitle( yName )
        self.hist.Draw(options)
        
    def GetBinLowEdges( self ):
        return np.array([ self.hist.GetBinLowEdge(i+1) for i in range(self.hist.GetNcells()) ])

    def GetBinCenters( self ):
        return np.array([ self.hist.GetBinCenter(i+1) for i in range(self.hist.GetNcells()) ])

    def GetBinCenterErrors( self ):
        return np.array([ self.hist.GetBinWidth(i+1) for i in range(self.hist.GetNcells()) ])/np.sqrt(12)

    def GetBinContents( self ):
        return np.array([ self.hist.GetBinContent(i+1) for i in range(self.hist.GetNcells()) ])

    def GetBinErrors( self ):
        return np.array([ self.hist.GetBinError(i+1) for i in range(self.hist.GetNcells()) ])

    def GetN( self ):
        return self.hist.GetNcells()

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
            raise TypeError("RHS {}({}) should be an instance of Histogram or Function".format(rhs, type(rhs)))
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
