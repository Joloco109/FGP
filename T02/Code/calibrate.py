from calibration import Calibration
from histogram import Histogram
import config as cfg
from finder import find_edges

def calibrate():
    opt_rausch, rausch = Histogram.Read( cfg.cali_dir+cfg.cali_rausch, "Rauschmessung", "Rauschmessung" )

    for f in cfg.cali_files:
        opt, hist = Histogram.Read( cfg.cali_dir+f, f[:-4], f[:-4] )
        hist -= opt.time / opt_rausch.time * rausch

        edges = find_edges( hist, 10, 10, 60 )

        hist.Draw()
        input()

if __name__ == "__main__":
    calibrate()
