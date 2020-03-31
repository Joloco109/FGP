import numpy as np

from config import cali_dir, cali_energy_file
#from enum import 

time_units= { 'Y' : 365, 'M' : 30, 'H' : 1/24 }

class Element:
    def __init__( self, name, decays ):
        self.name = name
        self.halftimes = np.zeros(len(decays))
        products = { "beta" : [], "gamma" : [] }
        
        for i in range(len(decays)):
            h = decays[i][0].split(' ')
            self.halftimes[i] = float(h[0]) * time_units[h[1]]
            for p in decays[i][1:]:
                products[p]

