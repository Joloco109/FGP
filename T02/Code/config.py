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


eff_dir = data_dir+"Effizienz/"
eff_files = ["Rauschen.TKA", "Effizienz.TKA"]
F_D = [4.91, 0.1 ] #cm²
r = [17, 1] #cm
A = [18.586*10**6, 0.005*10**6]
I_gamma = [0.805, 0]

comp_c_dir = data_dir + "Compton Conventional"
conv_files_Alu = [
        [50, "50Alu.TKA"],
        [60, "60Alu.TKA"],
        [80, "80Alu.TKA"],
        [90, "90Alu.TKA"],
        [105, "105Alu.TKA"]
    ]
conv_files_Steel = [
        [50, "50Stahl.TKA"],
        [60, "60Stahl.TKA"],
        [80, "80Stahl.TKA"],
        [90, "90Stahl.TKA"],
        [105, "105Stahl.TKA"]
    ]
conv_noise = [
        [50, "50Untergrund.TKA"]
        [60, "60Untergrund.TKA"]
        [80, "80Untergrund.TKA"]
        [90, "90Untergrund.TKA"]
        [105, "105Untergrund.TKA"]
        
        ]
