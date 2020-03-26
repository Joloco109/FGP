from ROOT import TF1, TCanvas, TLegend
from graph import MultiGraph, Graph
from function import Function
import numpy as np

eVolt = 1.602176e-19
k_boltzmann = 1.380649e-23

data_dir = "Data/"

cali_data = [
        "RT_left_setup.txt",
        "N_cal.txt",
        "He_cal.txt"
        ]

with open(data_dir+"RT_Value_K.txt") as f:
    cali_temps = [
            ( float( f.read().strip()[:-1] ),
                0.1/np.sqrt(12)),
            ( 77, 1/np.sqrt(12)),
            ( 4.2, 0.1/np.sqrt(12) ) ]

class Calibration(Function):
    def __init__( self, graph, function ):
        self.graph = graph
        self.function = function

    def Draw( self ):
        self.graph.Draw()

    def GetNDF( self ):
        return self.function.GetNDF()

    def GetChisquare( self ):
        return self.function.GetChisquare()

    def ArrayFromPointer( self, pointer ):
        return np.array( np.fromiter(
            pointer,
            dtype=np.float64,
            count=self.function.GetNpar()
            ) )

    def GetParameters( self ):
        return self.ArrayFromPointer( self.function.GetParameters() )

    def GetParErrors( self ):
        return self.ArrayFromPointer( self.function.GetParErrors() )

    def GetXaxis( self ):
        return self.graph.GetXaxis()

    def GetYaxis( self ):
        return self.graph.GetYaxis()

def calibrate( func, temps, resistance, column, y_name, out=False ):
    y_names = [ y_name if i == column else None  for i in range(7) ]

    data_res = np.zeros(len(temps))
    error_res = np.zeros(len(temps))
    data_tem = np.zeros(len(temps))
    error_tem = np.zeros(len(temps))

    for i, temp, file_name in zip(range(len(temps)),temps, resistance):
        res = MultiGraph.Read( data_dir+file_name, lambda x:1, y_names=y_names ).GetY(0)
        res = ( res.mean(), res.std() )
        data_res[i] = res[0]
        error_res[i] = res[1]
        data_tem[i] = temp[0]
        error_tem[i] = temp[1]

    if out:
        print("Data:")
        for temp, sig_temp, res, sig_res in zip( data_tem, error_tem, data_res, error_res ):
            print( (temp, sig_temp, res, sig_res) )
        print()

    calibration_graph = Graph( "Calibration " + y_name,
            data_tem, data_res,
            error_tem, error_res )

    calibration_graph.graph.Fit( func )

    xAxis = calibration_graph.GetXaxis()
    yAxis = calibration_graph.GetYaxis()
    xAxis.SetLimits( 0, 325 )
    xAxis.SetTitle( "T/K" )
    yAxis.SetTitle( "R/\\Omega" )
    xAxis.SetTitleSize(0.06)
    yAxis.SetTitleSize(0.06)
    xAxis.SetTitleOffset(0.80)
    yAxis.SetTitleOffset(0.84)
    xAxis.SetLabelSize(0.055)
    yAxis.SetLabelSize(0.055)

    return Calibration( calibration_graph, func )

def calibrate_C( out=False ):
    func = TF1("Calibration C", "[0]+[1]*e^(-[2]/x)")
    func.SetParameter( 0, 4000 )
    func.SetParameter( 1, -3000 )
    func.SetParameter( 2, 1e-4*(eVolt/k_boltzmann)/2 )
    calibration = calibrate( func, cali_temps, cali_data, 1, "C", out=out )
    return calibration

def calibrate_Pt( out=False ):
    func = TF1("Calibration Pt", "[0]+[1]*x")
    calibration = calibrate( func, cali_temps[:2], cali_data[:2], 0, "Pt", out=out )
    return calibration

def main():
    canvas = TCanvas("Calibration", "Calibration" )
    canvas.Divide(0,2)

    print("Calibration C:")
    caliC = calibrate_C( out=True )
    paras = caliC.GetParameters()
    sigParas = caliC.GetParErrors()
    print("A = {:7.2f} +- {:7.2f}".format(paras[0], sigParas[0]))
    print("B = {:7.2f} +- {:7.2f}".format(paras[1], sigParas[1]))
    print("C = {:7.4f} +- {:7.4f}".format(paras[2], sigParas[2]))
    if caliC.GetNDF() == 0:
        print("Chi = {:4.2f}".format(caliC.GetChisquare()))
        print("You overfitted with laughable few data points!\nWhat did you expect?")
    else:
        print("Chi/Ndf = {:4.2f}".format(caliC.GetChisquare()/caliC.GetNDF()))
    print()
    canvas.cd(1)
    caliC.Draw()
    legendC = TLegend(.40,.77,.60,.92)
    legendC.AddEntry(caliC.graph.graph, "Data")
    legendC.AddEntry(caliC.function, r"R = A + B e^{-C/T}")
    legendC.Draw()

    print("Calibration Pt:")
    caliPt = calibrate_Pt( out=True )
    paras = caliPt.GetParameters()
    sigParas = caliPt.GetParErrors()
    print("A = {:7.4f} +- {:7.4f}".format(paras[0], sigParas[0]))
    print("B = {:7.4f} +- {:7.4f}".format(paras[1], sigParas[1]))
    if caliPt.GetNDF() == 0:
        print("Chi = {:4.2f}".format(caliPt.GetChisquare()))
        print("You overfitted with laughable few data points!\nWhat did you expect?")
    else:
        print("Chi/Ndf = {:4.2f}".format(caliPt.GetChisquare()/caliPt.GetNDF()))
    print()
    canvas.cd(2)
    caliPt.Draw()
    legendPt = TLegend(.40,.77,.60,.92)
    legendPt.AddEntry(caliPt.graph.graph, "Data")
    legendPt.AddEntry(caliPt.function, r"R = A + B T")
    legendPt.Draw()

    canvas.Update()
    canvas.SaveAs("Graphs/calibration.eps")
    input()


if __name__ == "__main__":
    main()
