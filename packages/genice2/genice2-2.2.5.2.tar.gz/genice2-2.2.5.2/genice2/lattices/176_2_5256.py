from genice2.cell import cellvectors
import genice2.lattices
import numpy as np
desc = {
    "ref": {
        "176_2_5256": "Engel 2018"
    },
    "usage": "No options available.",
    "brief": "Hypothetical zeolitic ice"
}


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.cell = cellvectors(
            a=20.78944,
            b=20.84214,
            c=16.97667,
            A=90.0,
            B=90.0,
            C=120.24997
        )
        self.waters = np.array([
            [-0.081221, 0.333415, 0.125000],
            [-0.340533, -0.414338, 0.125000],
            [-0.666643, 0.414036, 0.375000],
            [0.073827, -0.334263, 0.375000],
            [-0.415023, -0.074694, 0.375000],
            [-0.674516, -0.089338, 0.375000],
            [-0.421594, -0.325738, 0.375001],
            [0.087986, 0.415155, 0.375000],
            [-0.333047, 0.089213, 0.125000],
            [-0.585667, 0.325838, 0.125000],
            [-0.592430, 0.074622, 0.125000],
            [-0.095868, -0.421626, 0.125000],
            [-0.081222, 0.333412, 0.624999],
            [-0.340533, -0.414338, 0.624999],
            [-0.666643, 0.414036, -0.125000],
            [0.073827, -0.334263, -0.125000],
            [-0.415023, -0.074694, -0.125000],
            [-0.674516, -0.089338, -0.125000],
            [-0.421594, -0.325738, -0.125000],
            [0.087986, 0.415155, -0.125000],
            [-0.333047, 0.089213, 0.624999],
            [-0.585667, 0.325838, 0.624999],
            [-0.592430, 0.074622, 0.624999],
            [-0.095868, -0.421626, 0.624999],
        ])
        self.coord = 'relative'
