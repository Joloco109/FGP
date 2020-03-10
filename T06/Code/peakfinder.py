from ROOT import TH1I, TF1
from reader import Hist

class Peaks:
    def __init__( self, hist, accuracy=10, peak_height=None ):
        self.acc = accuracy
        self.height = peak_height
        self.N = hist.hist.GetNcells()
        self.data = [ (i,hist.hist.GetBinContent( i )) for i in range(self.N) ]

    def __iter__(self):
        return self

    def __next__(self):
        maximum, max_val = max(self.data, key=lambda x : x[1] )

        n = maximum
        sum_old = float("inf")
        while n < self.N-self.acc:
            sum_new = sum( [ x[1] for x in self.data[ n: n+self.acc ] ] )
            if sum_new <= float("-inf"):
                while self.data[n][1] > float("-inf"):
                    n += 1
                break
            elif sum_new > sum_old:
                while self.data[n-1][1] >= self.data[n][1]:
                    n += 1
                break
            else:
                sum_old = sum_new
                n += self.acc
        upper = n

        n = maximum
        sum_old = float("inf")
        while n >= self.acc:
            sum_new = sum( [ x[1] for x in self.data[ n-self.acc: n ] ] )
            if sum_new <= float("-inf"):
                while self.data[n-1][1] > float("-inf"):
                    n -= 1
                break
            elif sum_new > sum_old:
                while self.data[n][1] >= self.data[n-1][1]:
                    n -= 1
                break
            else:
                sum_old = sum_new
                n -= self.acc
        lower = n

        edge = [ x[1] for x in self.data[lower:lower+self.acc] ]
        edge.extend( [ x[1] for x in self.data[upper-self.acc:upper] ] )
        if self.height != None and max_val - sum(edge)/(2*self.acc) < self.height:
            raise StopIteration

        self.data[lower:upper] = [ (0,float("-inf")) for i,n in self.data[lower:upper] ]

        return (lower,upper, maximum, max_val)

max_peak_number = 3

def peak_fit( hist, accuracy=10, peak_height=1e2, peak_fac = 10 ):
    peaks = [ peak for peak in Peaks( hist, accuracy=accuracy, peak_height=peak_height ) ]
    peaks.sort( key=lambda x : x[0] )
    peaks = [ (
        hist.hist.GetBinLowEdge(peak[0]),
        hist.hist.GetBinLowEdge(peak[1]),
        hist.hist.GetBinLowEdge(peak[2]),
        peak[3] ) for peak in peaks ]

    fits = []
    i = 0
    while i < len(peaks):
        j = 1
        start, end = peaks[i][:2]
        cur_func = "[0] + gaus(1)"
        max_vals = [ peaks[i][3] ]
        max_pos = [ peaks[i][2] ]
        widths = [ min( peaks[i][1] - peaks[i][2], peaks[i][2]-peaks[i][0]) ]

        while i+1 < len(peaks) and (
                end >= peaks[i+1][0]
                ) and (
                max(max_vals[-1], peaks[i+1][3])/min(max_vals[-1], peaks[i+1][3]) < peak_fac
                ):
            i += 1
            end = peaks[i][1]
            cur_func += " + gaus({})".format(3*j+1)
            max_vals.append( peaks[i][3] )
            max_pos.append( peaks[i][2] )
            widths.append( min( peaks[i][1] - peaks[i][2], peaks[i][2]-peaks[i][0]) )
            j += 1
            if j >= max_peak_number:
                break

        fit = TF1("peak_{}".format(i), cur_func, start, end)
        fit.SetParameter( 0, 0 )
        for k in range(j):
            fit.SetParameter( 3*k+1, max_vals[k] )
            fit.SetParLimits( 3*k+1, 0, 10*max_vals[k] )
            fit.SetParameter( 3*k+2, max_pos[k] )
            fit.SetParLimits( 3*k+2, max_pos[k] - widths[k], max_pos[k] + widths[k] )
            fit.SetParameter( 3*k+3, widths[k] )
            fit.SetParLimits( 3*k+3, 0, 100*widths[k] )
        fits.append( fit )
        i += 1

    for f in fits:
        hist.hist.Fit( f, "R+" )
    return fits
