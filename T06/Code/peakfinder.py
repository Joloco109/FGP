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

        avg = float("inf")
        avg_new = self.acc * max_val
        i = maximum + self.acc
        while avg >= avg_new and i < self.N:
            if self.data[i][1] <= float("-inf"):
                for j in range( i-self.acc, i, 1 ):
                    if self.data[j][1] > float("-inf"):
                        i = j + 1 + self.acc
                        break
                break
            avg = avg_new
            data = [ self.data[j][1] for j in range(i-self.acc, i)]
            avg_new = sum( self.data[i-self.acc : i][1] )
            avg_new = sum( data )
            i += self.acc
        upper = i-self.acc

        avg = float("inf")
        avg_new = self.acc * self.data[maximum][1]
        i = maximum - self.acc
        while avg >= avg_new and i > 0:
            if self.data[i][1] <= float("-inf"):
                for j in range( i+self.acc, i, -1 ):
                    if self.data[j][1] > float("-inf"):
                        i = j - self.acc
                        break
                break
            avg = avg_new
            data = [ self.data[j][1] for j in range(i, i+self.acc)]
            avg_new = sum( self.data[i : i+self.acc][1] )
            avg_new = sum( data )
            i -= self.acc
        lower = i+self.acc

        edge = [ x[1] for x in self.data[lower:lower+self.acc] ]
        edge.extend( [ x[1] for x in self.data[upper-self.acc:upper] ] )
        if self.height != None and max_val - sum(edge)/(2*self.acc) < self.height:
            raise StopIteration

        self.data[lower:upper] = [ (0,float("-inf")) for i,n in self.data[lower:upper] ]

        return (lower,upper, max_val)

def peak_fit( func, hist, accuracy=10, peak_height=None ):
    peaks = [ peak for peak in Peaks( hist, accuracy=accuracy, peak_height=peak_height ) ]
    peaks.sort( key=lambda x : x[0] )
    peaks = [ (
        hist.hist.GetBinLowEdge(peak[0]),
        hist.hist.GetBinLowEdge(peak[1]),
        peak[2] ) for peak in peaks ]

    fits = []
    for i in range(len(peaks)):
        fit = TF1("peak_{}".format(i), "gaus(0) + [3]", peaks[i][0], peaks[i][1] )
        fit.SetParameters( peaks[i][2], (peaks[i][0]+peaks[i][1])/2, (peaks[i][1]-peaks[i][0])/2, 0 )
        fit.SetParLimits( 2, 0, 10*(peaks[i][1]-peaks[i][0]) )
        fits.append( fit )

    for f in fits:
        hist.hist.Fit( f, "R+" )
    return fits
