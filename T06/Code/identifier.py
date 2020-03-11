import numpy as np
from calibrate import calibrate
from lit_values_reader import read_tabular, lit_file
from bayesian_inf import ModelDist


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
            None,
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

paras = [ ( 5, 1.5e2, 5 ),
        ( 5, 5e1, 5 )]

def spectral_line( elems=None, trans=None ):
    lit_tab = read_tabular(lit_file)
    lit_tab = [ [ column[i] for _, column in lit_tab ] for i in range(len(lit_tab[0][1])) ]
    if not elems == None:
        lit_tab = [ row for row in lit_tab if row[0] in elems  ]
    if not trans == None:
        if isinstance( trans[0], tuple ) :
            lit_tab = sum([ [ row for row in lit_tab if (row[0] == e and row[2] in t) ] for e,t in trans ], [])
        else:
            lit_tab = [ row for row in lit_tab if row[2] in trans ]
    lit_tab = [ (
        x[0], None if x[1]==None else int(x[1]), x[2],
        None if x[3]==None else float(x[3]), None if x[3]==None else float(x[4]),
        None if x[5]==None else float(x[5]), None if x[5]==None else float(x[6]),
        None if x[7]==None else float(x[7]), None if x[7]==None else float(x[8]),
        None if x[9]==None else float(x[9]), None if x[9]==None else float(x[10]),
        x[11]
        ) for x in lit_tab ]
    return lit_tab

def identify_peak( peak, lines ):
    energies = [ ((l[0],l[2]), [( l[3], l[4] )]) for l in lines ]

    model = ModelDist( energies )
    model.Update( (peak[0], np.sqrt(peak[1]**2+peak[2]**2)) )
    return model.Result()
