from ROOT import TF1
from graph import MultiGraph, Graph
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
            ( 77.15, 0.01),
            ( 4.2, 0.01 ) ]

class Calibration:
    def __init__( self, graph, function ):
        self.graph = graph
        self.function = function

    def Draw( self ):
        self.graph.Draw()

    def Get( self, x ):
        return (
                self.function.Eval( x[0] ),
                np.abs(self.function.Derivative( x[0] )) * x[1]
                )

    def GetX( self, y ):
        x = self.function.GetX( y[0], 0, 1e5 )
        return ( x,
                y[1] / np.abs(self.function.Derivative( x ))
                )

    def GetNDF( self ):
        return self.function.GetNDF()

    def GetChisquare( self ):
        return self.function.GetChisquare()

    def GetParameters( self ):
        return self.ArrayFromPointer( self.function.GetParameters() )

    def GetParErrors( self ):
        return self.ArrayFromPointer( self.function.GetParErrors() )

    def ArrayFromPointer( self, pointer ):
        return np.array( np.fromiter(
            pointer,
            dtype=np.float64,
            count=self.function.GetNpar()
            ) )

def calibrate( func, temps, resistance, column, y_name ):
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

    calibration_graph = Graph( "Calibration " + y_name,
            data_tem, data_res,
            error_tem, error_res )

    calibration_graph.graph.Fit( func )

    return Calibration( calibration_graph, func )

def calibrate_C():
    func = TF1("Calibration C", "[0]+[1]*e^(-[2]/x)")
    func.SetParameter( 0, 1000 )
    func.SetParameter( 1, 2000 )
    func.SetParameter( 2, 1e-4*(eVolt/k_boltzmann)/2 )
    calibration = calibrate( func, cali_temps, cali_data, 1, "C" )
    calibration.Draw()
    return calibration

def calibrate_Pt():
    func = TF1("Calibration Pt", "[0]+[1]*x")
    calibration = calibrate( func, cali_temps[:2], cali_data[:2], 0, "Pt" )
    calibration.Draw()
    return calibration

def main():
    print("Calibration C:")
    caliC = calibrate_C()
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

    print("Calibration Pt:")
    caliPt = calibrate_Pt()
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


if __name__ == "__main__":
    main()
