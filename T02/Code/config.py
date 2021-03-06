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
cali_marker = {"137Cs": 7, "60Co": 4, "152Eu": 6, "22Na": 3, "Peak": 24, "Compton": 25, "Backscatter": 26}


eff_dir = data_dir+"Effizienz/"
eff_files = ["Rauschen.TKA", "Effizienz.TKA"]
F_D = [4.91, 0.1 ] #cm²
r = [17, 1] #cm

A = [18.586*10**6, 0.005*10**6]
I_gamma = [0.805, 0]

comp_peaks = "compton_peaks.json"
att_coeff = "attenuation_coefficient.json"

u = 1.660539e-27*1e3
N = { "Alu" : (26.982, 0.001),
        "Steel" : (55.8, 0.5)
}
Z = { "Alu" : 13,
        "Steel" : 26
}
densities = {
        "Air" : ( 1.20e-3, 0.04e-3),
        "Steel":( 7.87,0.5),
        "Alu" : ( 2.70,0.1)
    }

comp_c_dir = data_dir + "Compton Conventional/"
conv_files_Alu = {
        50: "50Alu.TKA",
        60: "60Alu.TKA",
        80: "80Alu.TKA",
        90: "90Alu.TKA",
        105: "105Alu.TKA"
    }
conv_files_Steel = {
        50: "50Stahl.TKA",
        60: "60Stahl.TKA",
        80: "80Stahl.TKA",
        90: "90Stahl.TKA",
        105: "105Stahl.TKA"
    }
conv_noise = {
        50: "50Untergrund.TKA",
        60: "60Untergrund.TKA",
        80: "80Untergrund.TKA",
        90: "90Untergrund.TKA",
        105: "105Untergrund.TKA"
        }

F_D_conv = (4.91, 0.1 )
r_0_conv = (5, 1)
r_conv = (12, 1)
d_conv = (1.2, 0.1)
h_conv = (2.1, 0.1)
eff_conv = (0.4107, 0.02557)
Ne_conv = { "Alu" : (1.86*10**24, 3.23*10**23),
        "Steel" : (5.4416*10**24, 9.44*10**23)
        }

ring_thickness = (1.5,0.1)

comp_r_dir = data_dir + "Compton Ring/"

F_D_ring = (51.3, 0.1)
ring_files = {
        #theta :  r s(halber weg quelle-detector) N_e filename
        (10.85, 0.19) : (( 6.65, 0.05), (70, 1), (7.36*10**25, 9.81*10**24), "11grad.TKA"),
        (18.81, 0.33) : ((11.60, 0.05), (70, 1), (1.28*10**26, 1.72*10**25), "18,82grad.TKA"),
        (29.79, 0.51) : (( 6.65, 0.05), (25, 1), (7.36*10**25, 9.81*10**24), "30grad.TKA"),
        (36.32, 0.63) : (( 8.20, 0.05), (25, 1), (9.08*10**25, 1.22*10**25), "36grad.TKA"),
        (49.78, 0.85) : ((11.60, 0.05), (25, 1), (1.28*10**26, 1.72*10**25), "50grad.TKA")
        }
ring_noise = {
        25: "25cm_untergrund.TKA",
        70: "70cm_untergrund.TKA"
        }
