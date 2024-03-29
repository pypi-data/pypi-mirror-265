"""
Data Source

[Methane A] Maynard-Casely, H. E. et al. The distorted close-packed crystal structure of methane A. J. Chem. Phys. 133, 064504 (2010).
[ice R] Mochizuki, K., Himoto, K. & Matsumoto, M. Diversity of transition pathways in the course of crystallization into ice VII. Phys. Chem. Chem. Phys. 16, 16419–16425 (2014).
"""

from genice2.cell import cellvectors
import genice2.lattices

desc = {
    "ref": {"Methane A": "Maynard-Casely 2010", "R": "Mochizuki 2014"},
    "usage": "No options available.",
    "brief": "Hypothetical ice R.",
    "test": ({"options": "--depol=optimal"},),
}


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.cell = """
        7.547382417065826 0 0
        0.08957203488361681 7.54685087967168 0
        0.08957203488361681 0.08851523136724358 7.546331774698035
        """
        self.waters = """
        0.7029999999999993 0.2040000000000006 0.08500000000000085
        0.08500000000000087 0.7029999999999994 0.20400000000000063
        0.2040000000000006 0.08500000000000087 0.7029999999999993
        0.41999999999999993 0.9380000000000006 0.07199999999999918
        0.07199999999999916 0.41999999999999993 0.9380000000000005
        0.9380000000000005 0.07199999999999918 0.4199999999999999
        0.4350000000000005 0.5190000000000001 0.18900000000000003
        0.18900000000000006 0.4350000000000005 0.5190000000000001
        0.519 0.18900000000000006 0.4350000000000005
        0.9529999999999994 0.7200000000000006 0.6259999999999994
        0.6259999999999994 0.9529999999999994 0.7200000000000005
        0.7200000000000005 0.6259999999999993 0.9529999999999994
        0.8390000000000004 0.44500000000000023 0.3179999999999996
        0.3179999999999996 0.8390000000000003 0.4450000000000003
        0.44500000000000023 0.31799999999999967 0.8390000000000003
        0.7010000000000005 0.8330000000000001 0.29100000000000037
        0.29100000000000037 0.7010000000000004 0.8330000000000002
        0.8330000000000002 0.29100000000000037 0.7010000000000004
        0.18599999999999994 0.18599999999999994 0.18599999999999994
        0.9529999999999994 0.9529999999999994 0.9529999999999994
        0.5749999999999993 0.5749999999999992 0.5749999999999992
        """
        self.coord = "relative"
        self.bondlen = 3.05
        self.density = 1.5

        self.cell = cellvectors(
            a=7.547382417065826,
            b=7.547382417065826,
            c=7.547382417065826,
            A=89.31999999999998,
            B=89.31999999999998,
            C=89.31999999999998,
        )
