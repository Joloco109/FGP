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