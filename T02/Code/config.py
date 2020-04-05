data_dir = "Data/"

cali_dir = data_dir+"Kalibrierung/"
cali_files = [
        [ "137Cs", "137Cs calibration.TKA" ],
        [ "60Co", "60Co calibration.TKA" ],
        [ "152Eu", "152Eu calibration.TKA" ],
        [ "22Na", "22Na calibration.TKA" ],
    ]
cali_rausch = "Rauschen.TKA"
cali_energy_file = "energies.json"
cali_extrema = "extrema.json"
cali_energy_extrema = "extrema_energies.json"
cali_marker = {"137Cs": 7, "60Co": 4, "152Eu": 6, "22Na": 3, "peak": 24, "comp": 25, "back": 26}


eff_dir = data_dir+"Effizenz"
eff_files = ["Effizenz.TKA", "Rauschen.TKA"]
F_D = [4.91, 0.1 ] #cm²
r = [17, 1] #cm
A = [18.586, 0.005]
I_gamma = [0.805, 0]
