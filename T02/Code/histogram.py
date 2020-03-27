import codecs
import numpy as np
from ROOT import TH1I

class DataOptions:
    def __init__( self, time ):
        self.time = time

class Histogram:
    def __init__( self, bins, name, title=None, calibration=None ):
        if title==None:
            title = name
            
        self.name = name
        self.title = title

        if calibration==None:
            self.hist = TH1I( self.name, self.title, len(bins), 0, len(bins) )
            self.cali = None
        else:
            self.hist = TH1I( self.name, self.title, len(bins), calibration.Eval(0), calibration.Eval(len(bins)) )
            self.cali = calibration

        for i in range(len(bins)):
            self.hist.SetBinContent( i+1, bins[i] )
        self.hist.Sumw2()
            

    def Read( file_name, name, title ):
        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = [ x.strip() for x in content]
        time = float(content[0])
        data = [ int(x) for x in content[1:] if not x=='' ]

        return DataOptions( time ), Histogram( data, name, title )

    def Clone( self ):
        h = Histogram( [], self.name, self.title, self.calibration )
        h.hist = self.hist.Clone()
        return c

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
        
    def GetBins( self ):
        return np.array([ self.hist.GetBinContent(i+1) for i in range(self.GetNcells()) ])

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
