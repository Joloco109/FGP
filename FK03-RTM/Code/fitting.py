import numpy as np
from scipy.optimize import curve_fit


def lineare_regression(x,y,ey):
    s   = sum(1./ey**2)
    sx  = sum(x/ey**2)
    sy  = sum(y/ey**2)
    sxx = sum(x**2/ey**2)
    sxy = sum(x*y/ey**2)
    delta = s*sxx-sx*sx
    b   = (sxx*sy-sx*sxy)/delta
    a   = (s*sxy-sx*sy)/delta
    eb  = np.sqrt(sxx/delta)
    ea  = np.sqrt(s/delta)
    cov = -sx/delta
    corr = cov/(ea*eb)
    chiq  = sum(((y-(a*x+b))/ey)**2)
    return(a,ea,b,eb,chiq,corr)

def lin_regression(x,y,ey):
    f = lambda x, a, b : a*x + b
    par, par_cov = curve_fit(f, x, y, sigma=ey)
    return par, par_cov

def prop_regression(x,y,ey):
    f = lambda x, a : a*x
    a, a_err = curve_fit(f, x, y, sigma=ey)
    return a[0], a_err[0][0]

