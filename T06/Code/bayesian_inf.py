import numpy as np

def gaussian( e, sig_e, eH, sig_eH ):
    return np.exp( -0.5*(e-eH)**2/(sig_e**2+sig_eH**2) )/np.sqrt(sig_e**2+sig_eH**2)

class ModelDist:
    def __init__( self, hypothesis, probs=None, pEForH=gaussian ):
        if probs == None:
            probs = np.ones(len(hypothesis))/len(hypothesis)
        elif not ( len(hypothesis)==len(probs) ):
            raise ValueError
        self.names = [ name for name, energies in hypothesis]
        self.Energies = [np.array([ E[0] for E in energies ]) for name, energies in hypothesis]
        self.sigma_E = [np.array([ E[1] for E in energies ]) for name, energies in hypothesis]
        self.Probs = np.array( probs )
        self.pEForH = pEForH
        self.measurement_probs = []

    def Update( self, energy ):
        p = []
        f = np.zeros(len(self.Probs))
        for eElem, sigma_eElem, i in zip(self.Energies, self.sigma_E, range(len(self.Probs))):
            p_e = self.pEForH( energy[0], energy[1], eElem, sigma_eElem )/ len(eElem)
            f[i] = np.sum( p_e )
            p.append(p_e*self.Probs[i])
        self.Probs *= f
        c = sum(self.Probs)
        if c == 0 :
            raise ValueError( "No Hypothesis fits, maybe to low Errors?" )
        self.Probs /= c
        self.measurement_probs.append([ p_e/c for p_e in p ])
        i = 0
        while i in range(len(self.Probs)):
            if self.Probs[i] <= 0:
                del self.names[i]
                del self.Energies[i]
                del self.sigma_E[i]
                self.Probs = np.delete( self.Probs, i )
            else:
                i += 1
        return self

    def Result( self ):
        res = list(zip(self.names, self.Probs))
        res.sort( key=lambda x: -x[1] )
        return res

    def Mean( self ):
        if not len(self.Energies[0]) == 1:
            raise ValueError
        return sum([ p*e for p,[e] in zip( self.Probs, self.Energies ) ])

    def Var( self ):
        e_mean = self.Mean()
        return sum([ p*(e-e_mean)**2 for p,[e] in zip( self.Probs, self.Energies ) ])

    def __str__(self):
        res = list(zip(self.names, self.Probs, self.Energies, self.sigma_E))
        res.sort( key=lambda x: -x[1] )
        res = [ (name, p, list(zip(energies, sigma_e))) for name, p, energies, sigma_e in res ]
        return "Dist:   "+"\t".join( [ str(x)+"\n" for x in res ] )

    def __repr__(self):
        return str(self)
