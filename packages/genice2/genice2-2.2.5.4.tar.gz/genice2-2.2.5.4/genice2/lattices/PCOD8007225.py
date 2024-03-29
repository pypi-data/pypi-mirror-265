from genice2.cell import cellvectors
import genice2.lattices
import numpy as np
desc = {
    "ref": {
        "PCOD8007225": "Engel 2018",
        "engel24": "Engel 2018"
    },
    "usage": "No options available.",
    "brief": "Hypothetical zeolitic ice"
}


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.cell = cellvectors(
            a=22.80073,
            b=25.44238,
            c=23.98662,
            A=99.1653,
            B=60.9086,
            C=107.344
        )
        self.waters = np.array([
            [0.224946, 0.472779, 0.271647],
            [0.366735, 0.005910, -0.487573],
            [0.133313, -0.000554, -0.481909],
            [0.473673, 0.333467, -0.331293],
            [0.274028, 0.284513, 0.256268],
            [0.133346, 0.253362, 0.018111],
            [0.479728, 0.086179, 0.169149],
            [0.219467, 0.216224, -0.230764],
            [0.367058, 0.257568, 0.012012],
            [0.138938, 0.455641, 0.106002],
            [0.360130, 0.302880, 0.425237],
            [0.126957, 0.198497, -0.393539],
            [0.373423, 0.056543, -0.074852],
            [0.026747, 0.419510, -0.143901],
            [0.019250, 0.172224, 0.362648],
            [0.282965, 0.033817, -0.242926],
            [0.724945, 0.472779, 0.271647],
            [0.866735, 0.005910, -0.487573],
            [0.633316, -0.000554, -0.481914],
            [-0.026326, 0.333467, -0.331293],
            [0.774028, 0.284513, 0.256268],
            [0.633346, 0.253363, 0.018111],
            [-0.020273, 0.086178, 0.169149],
            [0.719470, 0.216224, -0.230765],
            [0.867058, 0.257568, 0.012011],
            [0.638942, 0.455645, 0.106002],
            [0.860132, 0.302881, 0.425237],
            [0.626957, 0.198497, -0.393540],
            [0.873424, 0.056543, -0.074851],
            [0.526748, 0.419510, -0.143901],
            [0.519251, 0.172224, 0.362648],
            [0.782971, 0.033820, -0.242926],
            [0.224946, -0.027220, 0.271645],
            [0.366735, 0.505913, -0.487573],
            [0.133313, 0.499446, -0.481909],
            [0.473673, -0.166533, -0.331293],
            [0.274028, -0.215486, 0.256268],
            [0.133346, -0.246638, 0.018111],
            [0.479727, 0.586178, 0.169149],
            [0.219468, 0.716225, -0.230765],
            [0.367057, -0.242430, 0.012013],
            [0.138938, -0.044358, 0.106001],
            [0.360131, -0.197120, 0.425237],
            [0.126957, 0.698496, -0.393539],
            [0.373424, 0.556545, -0.074852],
            [0.026748, -0.080489, -0.143902],
            [0.019249, 0.672222, 0.362648],
            [0.282964, 0.533817, -0.242926],
            [0.724947, -0.027220, 0.271645],
            [0.866735, 0.505913, -0.487573],
            [0.633314, 0.499446, -0.481909],
            [-0.026326, -0.166533, -0.331294],
            [0.774029, -0.215486, 0.256268],
            [0.633346, -0.246638, 0.018110],
            [-0.020273, 0.586178, 0.169150],
            [0.719468, 0.716225, -0.230765],
            [0.867059, -0.242430, 0.012013],
            [0.638937, -0.044359, 0.106001],
            [0.860132, -0.197120, 0.425237],
            [0.626957, 0.698496, -0.393539],
            [0.873424, 0.556545, -0.074851],
            [0.526750, -0.080488, -0.143902],
            [0.519250, 0.672222, 0.362648],
            [0.782970, 0.533821, -0.242925],
        ])
        self.coord = 'relative'
