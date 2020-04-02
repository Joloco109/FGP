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

def edge_fit( hist, edges, right=False ):
    fits = []
    for (start, end), i in zip(edges, range(len(edges))):

        # convolution (Faltung) of a triangle function with a gaussian normal distribution:
        # int from a to a+d:
        #   c*(y-a)/d * 1/sqrt(2)*sig * exp((x-y)^2/2*sig^2 ) dy
        # = c/2d *( (x-a)(erf(x/(sqrt(3)sig)) + erf((d-x)/(sqrt(2)sig))) + sqrt(2/pi) sig*(e^-(x^2/2sig^2) - e^-((d-x)^2/2sig^2) ) )
        # int from a-d to a:
        #   c*(a-y)/d * 1/sqrt(2)*sig * exp((x-y)^2/2*sig^2 ) dy
        # = c/2d *( (x-a)(erf(x/(sqrt(3)sig)) - erf((d+x)/(sqrt(2)sig))) + sqrt(2/pi) sig*(e^-(x^2/2sig^2) - e^-((d+x)^2/2sig^2) ) )

        function = "[0]+[1]*(\n\t(x-[2])*(\n{}\n\t)\n\t+ sqrt(2/pi)*[4]*(\n{}\n\t)\n)".format(
                    "\t\tTMath::Erf((x-[2])/(sqrt(2)*[4]))\n\t\t{} TMath::Erf( ([3] {} (x-[2]))/(sqrt(2)*[4]) )".format(
                        *(('+','-') if right else ('-','+')) ),
                    "\t\texp( -(x-[2])^2/(2*[4]^2) )\n\t\t+ exp( -([3] {} (x-[2]))^2/(2*[4]^2) )".format(
                        '-' if right else '+' ),
                )

        fit = TF1("edge_{}{}".format( 'B' if right else 'C', i), function, start, end)
        fit.SetParameter( 0, 500 )
        #fit.FixParameter( 0, 0 )
        #fit.SetParLimits( 0, 500, 500 )
        maximum = np.max(hist.Slice(start,end).GetBinContents())-500
        a = start if right else end
        d = (end-start)
        fit.SetParameter( 1, maximum/(2*d) )  # [1] = c/2d
        #fit.SetParLimits( 1, 0.8*maximum/(2*d), maximum/(2*d) )
        fit.SetParameter( 2, a ) # [2] = a
        #fit.SetParLimits( 2, start, end )
        fit.SetParameter( 3, d ) # [3] = d
        #fit.SetParLimits( 3, 0, 1000 )
        fit.SetParameter( 4, 10 ) # [4] = sig
        #fit.SetParLimits( 4, 0, 20 )

        fit = Function( fit )
        hist.Fit( fit, options="R+" )

        fits.append( fit )
    return fits
