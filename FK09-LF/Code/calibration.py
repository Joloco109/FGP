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

    return calibration_graph, func

def calibrate_C():
    func = TF1("Calibration C", "[0]+[1]*e^(-[2]/x)")
    func.SetParameter( 0, 1000 )
    func.SetParameter( 1, 2000 )
    func.SetParameter( 2, 1e-4*(eVolt/k_boltzmann)/2 )
    graph, calibration = calibrate( func, cali_temps, cali_data, 1, "C" )
    graph.Draw()
    return calibration

def calibrate_Pt():
    func = TF1("Calibration Pt", "[0]+[1]*x")
    graph, calibration = calibrate( func, cali_temps[:2], cali_data[:2], 0, "Pt" )
    graph.Draw()
