"""

Command line: /Users/matto/anaconda3/envs/genice/bin/genice2 T2D --dens 1.5127 -f p
Reshaping the unit cell.
  i:[1 0 0]
  j:[0 1 0]
  k:[0 0 1]
"""

from genice2.cell import cellvectors
import genice2.lattices

desc = {
    "ref": {"T2": "Yagasaki 2018"},
    "usage": "No options available.",
    "brief": "Hypothetical ice T2.",
    "test": ({"options": "--depol=optimal"},),
}


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.bondlen = 2.8577528998751287
        self.coord = "relative"
        self.cell = "19.91215483 19.91215483 7.57505890"
        self.density = 1.5127
        self.waters = """
            0.7040    0.6850    0.9660
            0.2960    0.3150    0.9660
            0.8150    0.7040    0.7160
            0.1850    0.2960    0.7160
            0.2960    0.6850    0.4660
            0.7040    0.3150    0.4660
            0.6850    0.2040    0.7160
            0.3150    0.7960    0.7160
            0.7960    0.3150    0.7840
            0.2040    0.6850    0.7840
            0.6850    0.2960    0.0340
            0.3150    0.7040    0.0340
            0.7040    0.8150    0.7840
            0.2960    0.1850    0.7840
            0.3150    0.2960    0.5340
            0.6850    0.7040    0.5340
            0.2040    0.1850    0.4660
            0.7960    0.8150    0.4660
            0.3150    0.2040    0.2160
            0.6850    0.7960    0.2160
            0.7960    0.1850    0.9660
            0.2040    0.8150    0.9660
            0.1850    0.7040    0.2160
            0.8150    0.2960    0.2160
            0.2960    0.8150    0.2840
            0.7040    0.1850    0.2840
            0.1850    0.7960    0.5340
            0.8150    0.2040    0.5340
            0.2040    0.3150    0.2840
            0.7960    0.6850    0.2840
            0.8150    0.7960    0.0340
            0.1850    0.2040    0.0340
            0.6090    0.3910    0.7500
            0.3910    0.6090    0.7500
            0.3910    0.3910    0.2500
            0.6090    0.6090    0.2500
            0.3910    0.1090    0.5000
            0.6090    0.8910    0.5000
            0.1090    0.6090    0.5000
            0.8910    0.3910    0.5000
            0.3910    0.8910    0.0000
            0.6090    0.1090    0.0000
            0.1090    0.8910    0.2500
            0.8910    0.1090    0.2500
            0.1090    0.3910    0.0000
            0.8910    0.6090    0.0000
            0.8910    0.8910    0.7500
            0.1090    0.1090    0.7500
            0.6110    0.5260    0.9570
            0.3890    0.4740    0.9570
            0.9740    0.6110    0.7070
            0.0260    0.3890    0.7070
            0.3890    0.5260    0.4570
            0.6110    0.4740    0.4570
            0.5260    0.1110    0.7070
            0.4740    0.8890    0.7070
            0.8890    0.4740    0.7930
            0.1110    0.5260    0.7930
            0.5260    0.3890    0.0430
            0.4740    0.6110    0.0430
            0.6110    0.9740    0.7930
            0.3890    0.0260    0.7930
            0.4740    0.3890    0.5430
            0.5260    0.6110    0.5430
            0.1110    0.0260    0.4570
            0.8890    0.9740    0.4570
            0.4740    0.1110    0.2070
            0.5260    0.8890    0.2070
            0.8890    0.0260    0.9570
            0.1110    0.9740    0.9570
            0.0260    0.6110    0.2070
            0.9740    0.3890    0.2070
            0.3890    0.9740    0.2930
            0.6110    0.0260    0.2930
            0.0260    0.8890    0.5430
            0.9740    0.1110    0.5430
            0.1110    0.4740    0.2930
            0.8890    0.5260    0.2930
            0.9740    0.8890    0.0430
            0.0260    0.1110    0.0430
            0.1740    0.5740    0.0970
            0.8260    0.4260    0.0970
            0.9260    0.1740    0.8470
            0.0740    0.8260    0.8470
            0.8260    0.5740    0.5970
            0.1740    0.4260    0.5970
            0.5740    0.6740    0.8470
            0.4260    0.3260    0.8470
            0.3260    0.4260    0.6530
            0.6740    0.5740    0.6530
            0.5740    0.8260    0.9030
            0.4260    0.1740    0.9030
            0.1740    0.9260    0.6530
            0.8260    0.0740    0.6530
            0.4260    0.8260    0.4030
            0.5740    0.1740    0.4030
            0.6740    0.0740    0.5970
            0.3260    0.9260    0.5970
            0.4260    0.6740    0.3470
            0.5740    0.3260    0.3470
            0.3260    0.0740    0.0970
            0.6740    0.9260    0.0970
            0.0740    0.1740    0.3470
            0.9260    0.8260    0.3470
            0.8260    0.9260    0.1530
            0.1740    0.0740    0.1530
            0.0740    0.3260    0.4030
            0.9260    0.6740    0.4030
            0.6740    0.4260    0.1530
            0.3260    0.5740    0.1530
            0.9260    0.3260    0.9030
            0.0740    0.6740    0.9030
            0.7350    0.5610    0.2940
            0.2650    0.4390    0.2940
            0.9390    0.7350    0.0440
            0.0610    0.2650    0.0440
            0.2650    0.5610    0.7940
            0.7350    0.4390    0.7940
            0.5610    0.2350    0.0440
            0.4390    0.7650    0.0440
            0.7650    0.4390    0.4560
            0.2350    0.5610    0.4560
            0.5610    0.2650    0.7060
            0.4390    0.7350    0.7060
            0.7350    0.9390    0.4560
            0.2650    0.0610    0.4560
            0.4390    0.2650    0.2060
            0.5610    0.7350    0.2060
            0.2350    0.0610    0.7940
            0.7650    0.9390    0.7940
            0.4390    0.2350    0.5440
            0.5610    0.7650    0.5440
            0.7650    0.0610    0.2940
            0.2350    0.9390    0.2940
            0.0610    0.7350    0.5440
            0.9390    0.2650    0.5440
            0.2650    0.9390    0.9560
            0.7350    0.0610    0.9560
            0.0610    0.7650    0.2060
            0.9390    0.2350    0.2060
            0.2350    0.4390    0.9560
            0.7650    0.5610    0.9560
            0.9390    0.7650    0.7060
            0.0610    0.2350    0.7060
            0.5000    0.5000    0.2500
            0.5000    0.5000    0.7500
            0.5000    0.0000    0.0000
            0.0000    0.5000    0.0000
            0.5000    0.0000    0.5000
            0.0000    0.0000    0.7500
            0.0000    0.5000    0.5000
            0.0000    0.0000    0.2500
        """

        self.cell = cellvectors(a=19.91215483, b=19.91215483, c=7.5750589)
