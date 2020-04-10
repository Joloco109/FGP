import numpy as np
import json

from config import cali_dir, cali_energy_file

time_units= { 'Y' : 365, 'M' : 30, 'H' : 1/24 }

class Element:
    def __init__( self, name, decays ):
        self.name = name
        self.halftimes = np.zeros(len(decays))
        self.products = { "beta" : [[],[],[]], "gamma" : [[],[],[]], "EC gamma" : [[],[],[]] }
        
        for i in range(len(decays)):
            if decays[i][0]==None:
                self.halftimes = None
            else :
                h = decays[i][0].split(' ')
                self.halftimes[i] = float(h[0]) * time_units[h[1]]
            for p in decays[i][1]:
                productlist = self.products[p[0]]
                for energy, sig_energy, intensity in p[2]:
                    productlist[0].append( energy )
                    productlist[1].append( sig_energy )
                    if not self.halftimes:
                        productlist[2].append( p[1]*intensity/100 )
                    else:
                        productlist[2].append( p[1]*intensity/100/self.halftimes[i] )

        for key in self.products:
            self.products[key] = np.array( self.products[key] )
            if self.halftimes:
                self.products[key][2] /= np.sum(1/self.halftimes)

    def Read( filename ):
        data = json.loads( open( filename ).read() )
        elements = [ Element( name, decays ) for name, *decays in data ]
        return elements

    def __repr__(self):
        ret = self.name + "\n\thalftimes: "
        if not self.halftimes==None:
            for h in self.halftimes[:-1]:
                ret += str(float(h))+", "
            ret += str(float(self.halftimes[-1])) + "\n"
        ret += "Products:"
        for key in self.products:
            ret += "\n\t"+key + ": "
            for p in self.products[key].T:
                ret += str({"E":p[0], "sig_E":p[1], "I":p[2]}) + ", "
        return ret
