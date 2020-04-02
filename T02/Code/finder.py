import numpy as np
from ROOT import TF1

from function import Function

def slope( x, y, w ):
    sumw2 = np.sum( w )
    if sumw2 >= np.inf:
        mask = tuple([w >= np.inf])
        x = x[mask]
        y = y[mask]
        sumw2 = 1
        w = np.ones(len(x))/len(x)

    x_bar = np.sum( w*x )/sumw2
    x2_bar = np.sum( w*(x**2) )/sumw2
    if not x2_bar == x_bar**2:
        m = np.sum( w*(x-x_bar)*y)/sumw2 /(x2_bar - x_bar**2)
        sig2_m = np.sum( w*(x-x_bar)**2)/sumw2**2 /(x2_bar - x_bar**2)**2
    else:
        m = 0
        sig2_m = 0
    return m, sig2_m


def find_edges( hist, acc, width, degree ):
    i = acc
    N = hist.GetN()

    centers = hist.GetBinCenters()
    centers /= np.max(centers)
    contents = hist.GetBinContents()
    errors = hist.GetBinErrors()

    max_cont = np.sum(np.sort(contents)[-10:-2])/8
    errors /= max_cont
    contents /= max_cont

    with np.errstate(divide='ignore'):
        weights = 1/errors**2

    while i < len(weights) - width - acc:
        m_last, sig2_m_last = slope( centers[i-acc:i], contents[i-acc:i], weights[i-acc:i] )
        m, sig2_m = slope( centers[i+width:i+width+acc], contents[i+width:i+width+acc], weights[i+width:i+width+acc] )
        #print(sig2_m_last, sig2_m)
        if np.sin( m ) - np.sin( m_last ) > degree/180*np.pi:
            print( "Rising at {}: from {:.3e}({:.2f}°) to {:.3e}({:.2f}°)".format(
                i,
                m_last, 180/np.pi*np.sin(m_last),
                m, 180/np.pi*np.sin(m)  )  )
            #i += acc
        if np.sin( m ) - np.sin( m_last ) < -degree/180*np.pi:
            print( "Sinking at {}: from {:.3e}({:.2f}°) to {:.3e}({:.2f}°)".format(
                i, 180/np.pi*m_last, np.sin(m_last),
                m, 180/np.pi*np.sin(m)  )  )
            #i += acc
        i += 1

def peak_fit( hist, peaks ):
    fits = []
    for (start, end), i in zip(peaks, range(len(peaks))):
        fit = TF1("peak_{}".format(i), "pol1 + gaus(2)", start, end)
        fit.SetParameter( 0, 0 )
        fit.SetParameter( 1, 0 )
        maximum = np.max(hist.GetBinContents())
        fit.SetParameter( 2, maximum )
        fit.SetParameter( 3, (start+end)/2 )
        fit.SetParameter( 4, (end-start)/2 )
        fit = Function( fit )
        hist.Fit( fit, options="R+" )

        fits.append( fit )
    return fits
