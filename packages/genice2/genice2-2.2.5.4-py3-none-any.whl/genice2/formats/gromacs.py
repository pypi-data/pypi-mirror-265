# coding: utf-8

from logging import getLogger

import genice2.formats
from genice2.decorators import banner, timeit
from genice2.molecules import serialize
from genice2.cell import cellvectors
import numpy as np

desc = {
    "ref": {"gro": "http://manual.gromacs.org/current/online/gro.html"},
    "brief": "Gromacs .gro file.",
    "usage": "No options available.",
}


class Format(genice2.formats.Format):
    """
    The atomic positions of the molecules are output in Gromacs format.
    No options available.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def hooks(self):
        return {7: self.Hook7}

    @timeit
    @banner
    def Hook7(self, ice):
        "Output in Gromacs format."
        logger = getLogger()
        cellmat = ice.repcell.mat

        if not (cellmat[0, 1] == 0 and cellmat[0, 2] == 0 and cellmat[1, 2] == 0):
            logger.info(
                "  The specified reshaping matrix does not obey the requirements for Gromacs' unit cell convention."
            )
            a = np.linalg.norm(cellmat[0])
            b = np.linalg.norm(cellmat[1])
            c = np.linalg.norm(cellmat[2])
            ea = cellmat[0] / a
            eb = cellmat[1] / b
            ec = cellmat[2] / c
            A = np.degrees(np.arccos(eb @ ec))
            B = np.degrees(np.arccos(ec @ ea))
            C = np.degrees(np.arccos(ea @ eb))
            rotmat = ice.repcell.inv @ cellvectors(a, b, c, A, B, C)
            logger.info("  The reshape matrix is reoriented.")
        else:
            rotmat = np.eye(3)

        atoms = []
        for mols in ice.universe:
            atoms += serialize(mols)

        logger.info("  Total number of atoms: {0}".format(len(atoms)))
        if len(atoms) > 99999:
            logger.warn(
                "  Fixed-digit format of Gromacs cannot deal with atoms more than 99999. Residue number and atom number are set appropriately."
            )
        s = ""
        s += "Generated by GenIce https://github.com/vitroid/GenIce \n"
        s += "{0}\n".format(len(atoms))
        molorder = 0
        for i, atom in enumerate(atoms):
            resno, resname, atomname, position, order = atom
            position = position @ rotmat
            if resno == 0:
                molorder += 1
            if len(atoms) > 99999:
                s += "{0:5d}{1:5s}{2:>5s}{3:5d}{4:8.3f}{5:8.3f}{6:8.3f}\n".format(
                    9999, resname, atomname, 9999, position[0], position[1], position[2]
                )
            else:
                s += "{0:5d}{1:5s}{2:>5s}{3:5d}{4:8.3f}{5:8.3f}{6:8.3f}\n".format(
                    molorder,
                    resname,
                    atomname,
                    i + 1,
                    position[0],
                    position[1],
                    position[2],
                )
        cellmat = cellmat @ rotmat
        if cellmat[1, 0] == 0 and cellmat[2, 0] == 0 and cellmat[2, 1] == 0:
            s += "    {0:.8f} {1:.8f} {2:.8f}\n".format(
                cellmat[0, 0], cellmat[1, 1], cellmat[2, 2]
            )
        else:
            s += "    {0:.8f} {1:.8f} {2:.8f} {3:.8f} {4:.8f} {5:.8f} {6:.8f} {7:.8f} {8:.8f}\n".format(
                cellmat[0, 0],
                cellmat[1, 1],
                cellmat[2, 2],
                cellmat[0, 1],
                cellmat[0, 2],
                cellmat[1, 0],
                cellmat[1, 2],
                cellmat[2, 0],
                cellmat[2, 1],
            )
        # s += '#' + "\n#".join(ice.doc) + "\n"
        self.output = s
