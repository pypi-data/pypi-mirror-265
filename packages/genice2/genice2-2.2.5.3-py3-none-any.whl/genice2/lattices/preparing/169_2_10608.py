from genice2.cell import cellvectors
import genice2.lattices
import numpy as np
desc = {
    "ref": {
        "169_2_10608": "Engel 2018",
        "engel12": "Engel 2018"
    },
    "usage": "No options available.",
    "brief": "Hypothetical zeolitic ice"
}


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.cell = np.array([
            [4.393378, 7.119216, -0.003994],
            [-4.017702, 7.052853, -0.005129],
            [-0.00154, 0.002506, 5.11708],
        ])
        self.waters = np.array([
            [0.389453, 0.174954, 0.008327],
            [-0.397473, -0.20097, -0.491436],
            [-0.411158, -0.425076, -0.151435],
            [0.402713, 0.399227, 0.348449],
            [0.167865, 0.411826, -0.321178],
            [-0.176019, -0.437183, 0.178531],
            [0.290858, -0.021084, 0.287134],
            [-0.298955, -0.00448, -0.213188],
            [0.28291, -0.298679, 0.085352],
            [-0.291019, 0.273074, -0.415163],
            [-0.011186, -0.283577, -0.057766],
            [0.003082, 0.258212, 0.442187],
        ])
        self.coord = 'relative'
