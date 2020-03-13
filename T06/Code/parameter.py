
data_dir = "Data/"
am_dir = "Am/"
roe_dir = "Röhre/"

leer_names = [
        "Leer.mca",
        "Leer.mca"
        ]

file_names = [ [
            "Kupfer.mca",
            "Silber.mca",
            "Stahl.mca",
            "Alu.mca",
            "Blei.mca",
            "Chip.mca",
            "Iod.mca",
            "Magnet.mca",
            "Molybdenium.mca",
            "Münze.mca",
            "Tigerauge.mca"
        ],[
            "Copper.mca",
            "Silber.mca",
            "Stahl.mca",
            "Barium.mca",
            "Molybden.mca",
            "Rubidium.mca",
            "Terbium.mca"
        ]
    ]

elements = [ [
            [ "Cu" ],
            [ "Ag" ],
            [ "Fe", "Mo", "Cr", "Ni" ],
            None,
            [ "Pb" ],
            None,
            None,
            None,
            None,
            None,
            None
        ],[
            [ "Cu" ],
            [ "Ag" ],
            [ "Fe", "Mo", "Cr", "Ni" ],
            [ "Ba" ],
            [ "Mo" ],
            [ "Rb" ],
            [ "Tb" ]
        ]
    ]

paras = [ [ ( 5, 1.5e2, 5, 10 ),
            ( 5, 1.5e2, 4, 10 ),
            ( 5, 1.5e2, 4, 10 ),
            ( 5, 1.5e2, 4, 10 ),
            ( 3, 14e2, 4, 10 ),
            ( 5, 1.5e2, 5, 10 ),
            ( 5, 1.5e2, 3, 10 ),
            ( 6, 1.5e2, 5, 10 ),
            ( 5, 1.5e2, 5, 10 ),
            ( 5, 1.5e2, 5, 10 ),
            ( 5, 1.5e2, 5, 10 )
        ], [
            ( 5, 5e1, 5, 10 ),
            ( 5, 5e1, 5, 10 ),
            ( 5, 5e1, 5, 10 ),
            ( 5, 5e1, 5, 10 ),
            ( 5, 5e1, 5, 10 ),
            ( 5, 5e1, 5, 10 ),
            ( 5, 3e1, 10, 10)
        ] ]

calibration_names = [ [
            "Kupfer.mca",
            "Silber.mca",
            "Stahl.mca"
        ],[
            "Copper.mca",
            "Silber.mca",
            "Stahl.mca",
            "Barium.mca",
            "Molybden.mca",
            "Rubidium.mca",
            "Terbium.mca"
        ]
    ]

calibration_elements = [ [
            [ "Cu" ],
            [ "Ag" ],
            [ "Fe", "Mo", "Cr", "Ni" ]
        ],[
            [ "Cu" ],
            [ "Ag" ],
            [ "Fe", "Mo", "Cr", "Ni" ],
            [ "Ba" ],
            [ "Mo" ],
            [ "Rb" ],
            [ "Tb" ]
        ]
    ]

calibration_peaks = [ [
            [ "KL3", "KM3" ],
            [ "L3M5", "L2M5", "KL2", "KM2", "KN1", None, None, None ],
            [ None,None,None,None,None,None,None,None,None,None ]
        ],[
            [ "KL3", "KM3" ],
            [ "KL3", "KM3", "KN3" ],
            [ None ],
            [ None,"KL2", "KL3", "KM3", "KN3" ],
            [ "KL3", "KM2" ],
            [ "KL2", "KM2" ],
            [ "L3M4", "L2M4", "L3N4", "KL2", "KL3", None ] #"KM3" ]
        ]
    ]

calibration_lines = [ [
            [ "K", "K" ],
            [ "L", "L", "K", "K", "K", None, None, None ],
            [ "K", "K", "K", "K", "K", "K", "K", "K",None,None ]
        ],[
            [ "K", "K" ],
            [ "K", "K", "K" ],
            [ ],
            [ None,"K", "K", "K", "K" ],
            [ "K", "K" ],
            [ "K", "K" ],
            [ "L", "L", "L", "K", "K", None ]
        ]
    ]
