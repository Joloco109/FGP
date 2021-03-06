import codecs
import numpy as np
from ROOT import TH1I

hist_file = "Data/Röhre/Kupfer.mca"
hist_file2 = "Data/Röhre/Leer.mca"

class Hist:
    def __init__( self, hist=None, name=None, title=None ):
        self.hist = hist
        if not name == None:
            self.hist.name = name
        if not title == None:
            self.hist.title = title

    def read( file_name, name, title, boundries=None, calibration=None ):
        hist = Hist()

        with codecs.open(file_name, 'r', 'iso-8859-1') as f:
            content = f.readlines()
        content = [ x.strip() for x in content]
        data = []
        while len(content) > 0:
            line = content.pop(0)
            if line == "<<DATA>>":
                while not content[0] == "<<END>>":
                    data.append(int(content.pop(0)))
                content.pop(0)
        

        if not calibration==None:
            if boundries == None:
                boundries = (
                        calibration.get( (0,0) )[0],
                        calibration.get( (len(data),0) )[0]
                        )
            else :
                data = data[ boundries[0]:boundries[1]]
                boundries = (
                    calibration.get( (boundries[0],0) )[0],
                    calibration.get( (boundries[1],0) )[0]
                    )
        else :
            boundries = (0, len(data))

        t_hist = TH1I(name, title, len(data), boundries[0], boundries[1])
        for i in range(len(data)):
            t_hist.SetBinContent(i+1, data[i])
        hist.hist = t_hist
        hist.hist.Sumw2()

        return hist

    def name(self):
        return self.hist.GetName()
