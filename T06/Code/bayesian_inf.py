import numpy as np

def gaussian( e, sig_e, eH, sig_eH ):
    return np.exp( -0.5*(e-eH)**2/(sig_e**2+sig_eH**2) )/np.sqrt(sig_e**2+sig_eH**2)

class ModelDist:
    def __init__( self, energies, probs=None, pEForH=gaussian ):
        if probs == None:
            probs = np.ones(len(energies))/len(energies)
        elif not ( len(energies)==len(probs) ):
            raise ValueError
        self.Energies = [np.array([ E[0] for E in hypothesis ]) for hypothesis in energies]
        self.sigma_E = [np.array([ E[1] for E in hypothesis ]) for hypothesis in energies]
        self.Probs = np.array( probs )
        self.pEForH = pEForH
        self.measurement_probs = []

    def Update( self, energy ):
        p = []
        f = np.zeros(len(self.Probs))
        for eElem, sigma_eElem, i in zip(self.Energies, self.sigma_E, range(len(self.Probs))):
            p_e = self.pEForH( energy[0], energy[1], eElem, sigma_eElem )/ len(eElem)
            f[i] = np.sum( p_e )
            p.append(p_e)
        self.Probs *= f
        c = sum(self.Probs)
        self.Probs /= c
        self.measurement_probs.append([ p_e/c for p_e in p ])
        return self
