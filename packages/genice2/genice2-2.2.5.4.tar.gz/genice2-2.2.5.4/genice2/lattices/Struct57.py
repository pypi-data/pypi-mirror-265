# coding: utf-8
"""
Data source: Dutour Sikirić, Mathieu, Olaf Delgado-Friedrichs, and Michel Deza. “Space Fullerenes: a Computer Search for New Frank-Kasper Structures” Acta Crystallographica Section A Foundations of Crystallography 66.Pt 5 (2010): 602–615.

Cage composition:
 (12,14,15,16) = (12,12,0,4,)
"""
from genice2.cell import cellvectors
import genice2.lattices
desc = {"ref": {"SpaceFullerene": 'Sikiric 2010'},
        "usage": "No options available.",
        "brief": "A space fullerene."
        }


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.pairs = """
        8 79
        132 124
        126 134
        61 149
        49 142
        48 36
        10 159
        136 104
        110 3
        28 18
        29 3
        41 149
        20 140
        67 72
        28 136
        34 68
        139 81
        152 71
        20 12
        131 133
        104 49
        72 14
        109 53
        152 133
        37 73
        86 121
        13 133
        134 145
        108 55
        106 54
        147 127
        135 151
        32 153
        21 45
        85 132
        8 55
        86 137
        92 48
        41 112
        126 14
        69 9
        159 142
        109 47
        83 94
        86 96
        17 58
        13 19
        102 143
        109 159
        46 149
        28 82
        78 50
        115 70
        108 142
        97 120
        44 53
        24 61
        17 158
        5 31
        115 126
        0 105
        137 101
        60 89
        31 53
        40 95
        48 156
        117 76
        26 49
        35 3
        35 73
        96 103
        84 89
        110 11
        127 68
        121 41
        78 36
        157 52
        144 96
        65 148
        69 112
        20 30
        83 46
        29 89
        16 73
        92 102
        22 74
        100 155
        109 148
        100 157
        63 62
        123 47
        117 87
        108 15
        106 21
        124 75
        1 150
        156 143
        107 25
        22 87
        11 0
        106 74
        52 111
        146 111
        133 81
        25 57
        91 140
        59 130
        125 116
        96 87
        144 49
        26 103
        0 129
        68 71
        2 131
        27 34
        18 137
        148 57
        115 153
        144 33
        67 73
        61 39
        131 45
        125 87
        43 45
        7 18
        23 8
        147 24
        8 113
        62 122
        29 127
        75 46
        141 3
        154 25
        74 77
        1 54
        86 139
        11 113
        34 155
        9 104
        107 32
        22 57
        156 50
        44 66
        60 135
        93 101
        93 88
        6 103
        148 77
        156 32
        100 72
        29 130
        102 123
        10 26
        136 78
        90 61
        107 93
        134 32
        7 40
        26 76
        150 56
        84 158
        154 82
        123 129
        89 138
        125 131
        124 40
        35 99
        27 98
        5 159
        151 146
        55 70
        121 39
        64 132
        134 66
        90 98
        128 84
        52 38
        92 4
        67 62
        94 152
        81 39
        78 65
        93 85
        38 79
        104 51
        120 98
        130 24
        64 46
        80 119
        55 51
        97 157
        88 9
        13 95
        18 41
        7 54
        125 139
        23 42
        74 103
        30 79
        2 95
        27 40
        10 77
        37 63
        12 35
        152 43
        16 59
        33 105
        36 77
        52 84
        147 19
        13 68
        150 75
        114 124
        16 94
        136 101
        7 56
        138 111
        6 116
        145 53
        118 70
        15 138
        155 62
        116 76
        129 118
        16 141
        4 47
        145 65
        9 76
        141 71
        150 122
        48 25
        63 75
        119 38
        97 128
        153 51
        108 11
        64 139
        129 151
        42 143
        141 135
        83 81
        12 90
        27 63
        60 59
        50 51
        110 138
        54 82
        2 22
        132 137
        44 146
        58 122
        17 71
        67 140
        30 99
        4 117
        119 14
        21 19
        144 101
        91 79
        1 45
        107 65
        60 118
        85 69
        23 50
        56 149
        64 112
        106 95
        114 154
        157 30
        142 105
        72 99
        33 88
        58 43
        126 113
        114 1
        114 2
        58 128
        0 115
        4 57
        19 39
        116 112
        59 140
        44 123
        80 146
        98 56
        97 34
        91 14
        117 33
        23 145
        31 111
        15 5
        21 6
        120 122
        128 127
        6 121
        147 43
        66 143
        80 158
        28 69
        47 105
        91 70
        12 130
        90 37
        99 113
        94 24
        31 42
        85 154
        110 151
        37 83
        42 38
        15 118
        20 120
        92 10
        66 119
        135 158
        100 80
        88 153
        17 155
        82 36
        102 5
        """

        self.waters = """
        0.8125 0.80241 0.19017
        0.5 0.25631 0.72057
        0.8125 0.19759 0.80983
        0.0 0.57611 0.125
        0.6875 0.97648 0.9375
        0.3125 0.82131 0.94195
        0.3125 0.17869 0.05805
        0.1875 0.24211 0.56695
        0.1875 0.75789 0.43305
        0.5 0.01882 0.28211
        0.3125 0.97648 0.9375
        0.0 0.74369 0.22057
        0.1875 0.50402 0.3125
        0.0 0.33606 0.9033
        0.6875 0.67813 0.49612
        0.3125 0.75789 0.06695
        0.6875 0.50402 0.1875
        0.6875 0.49598 0.8125
        0.1875 0.17869 0.44195
        0.1875 0.32187 0.99612
        0.3125 0.53806 0.4375
        0.3125 0.24211 0.93305
        0.875 0.11065 0.87233
        0.1875 0.82131 0.55805
        0.375 0.41372 0.15533
        0.6875 0.03293 0.6875
        0.3125 0.02352 0.0625
        0.0 0.37164 0.59468
        0.3125 0.10594 0.47228
        0.1875 0.53806 0.0625
        0.1875 0.60732 0.49879
        0.1875 0.77679 0.81517
        0.6875 0.89406 0.52773
        0.8125 0.96707 0.1875
        0.0 0.44091 0.71903
        0.0 0.55909 0.28097
        0.3125 0.03293 0.6875
        0.875 0.41372 0.34468
        0.375 0.69233 0.6533
        0.125 0.30767 0.1533
        0.0 0.27487 0.62678
        0.3125 0.22321 0.31517
        0.3125 0.77679 0.68483
        0.5 0.37164 0.90533
        0.8125 0.77679 0.81517
        0.5 0.27487 0.87322
        0.625 0.30767 0.3467
        0.8125 0.89406 0.97228
        0.5 0.98118 0.7179
        0.1875 0.96707 0.1875
        0.3125 0.89406 0.52773
        0.375 0.88936 0.37233
        0.25 0.63854 0.75
        0.0 0.82602 0.783
        0.3125 0.19759 0.69017
        0.3125 0.80241 0.30983
        0.3125 0.32187 0.50388
        0.8125 0.03293 0.8125
        0.5 0.44091 0.78097
        0.5 0.55909 0.21903
        0.5 0.62836 0.09468
        0.25 0.36147 0.25
        0.6875 0.46195 0.5625
        0.8125 0.39268 0.50121
        0.6875 0.22321 0.31517
        0.0 0.95296 0.625
        0.6875 0.77679 0.68483
        0.6875 0.53806 0.4375
        0.0 0.42389 0.875
        0.5 0.10124 0.37767
        0.5 0.74369 0.27944
        0.8125 0.46195 0.9375
        0.8125 0.60732 0.49879
        0.8125 0.50402 0.3125
        0.125 0.11065 0.87233
        0.6875 0.32187 0.50388
        0.5 0.04705 0.125
        0.1875 0.03293 0.8125
        0.1875 0.97648 0.5625
        0.3125 0.67813 0.49612
        0.75 0.63854 0.75
        0.875 0.30767 0.1533
        0.375 0.11065 0.62767
        0.75 0.36147 0.25
        0.375 0.58629 0.84468
        0.6875 0.10594 0.47228
        0.0 0.17399 0.21701
        0.8125 0.10594 0.02773
        0.6875 0.96707 0.3125
        0.3125 0.60732 0.00121
        0.125 0.41372 0.34468
        0.5 0.66394 0.4033
        0.5 0.95296 0.875
        0.8125 0.02352 0.4375
        0.625 0.41372 0.15533
        0.0 0.25631 0.77944
        0.0 0.10124 0.12233
        0.1875 0.49598 0.6875
        0.1875 0.39268 0.50121
        0.0 0.62836 0.40533
        0.875 0.58629 0.65533
        0.0 0.04705 0.375
        0.5 0.85198 0.87678
        0.1875 0.10594 0.02773
        0.3125 0.96707 0.3125
        0.875 0.88936 0.12767
        0.1875 0.19759 0.80983
        0.8125 0.97648 0.5625
        0.1875 0.80241 0.19017
        0.0 0.89877 0.87767
        0.0 0.66394 0.0967
        0.125 0.69233 0.8467
        0.5 0.17399 0.283
        0.0 0.72513 0.37322
        0.6875 0.19759 0.69017
        0.6875 0.80241 0.30983
        0.5 0.14802 0.12322
        0.6875 0.02352 0.0625
        0.5 0.72513 0.12678
        0.625 0.69233 0.6533
        0.3125 0.46195 0.5625
        0.1875 0.22321 0.18483
        0.5 0.42389 0.625
        0.6875 0.82131 0.94195
        0.8125 0.24211 0.56695
        0.6875 0.17869 0.05805
        0.8125 0.75789 0.43305
        0.1875 0.46195 0.9375
        0.3125 0.49598 0.8125
        0.6875 0.75789 0.06695
        0.3125 0.50402 0.1875
        0.6875 0.24211 0.93305
        0.8125 0.17869 0.44195
        0.8125 0.32187 0.99612
        0.8125 0.82131 0.55805
        0.6875 0.60732 0.00121
        0.1875 0.02352 0.4375
        0.0 0.14802 0.37678
        0.1875 0.67813 0.00388
        0.8125 0.22321 0.18483
        0.5 0.57611 0.375
        0.8125 0.53806 0.0625
        0.125 0.88936 0.12767
        0.5 0.82602 0.71701
        0.0 0.01882 0.2179
        0.0 0.85198 0.62322
        0.875 0.69233 0.8467
        0.3125 0.39268 0.99879
        0.0 0.98118 0.78211
        0.375 0.30767 0.3467
        0.5 0.33606 0.5967
        0.8125 0.67813 0.00388
        0.6875 0.39268 0.99879
        0.625 0.88936 0.37233
        0.625 0.11065 0.62767
        0.8125 0.49598 0.6875
        0.5 0.89877 0.62233
        0.125 0.58629 0.65533
        0.625 0.58629 0.84468
        0.1875 0.89406 0.97228
        """

        self.coord = "relative"

        self.cages = """
        12 0.0 -0.21676 1.01068
        14 0.0 0.43193 0.12387
        14 -0.25 -0.65222 -0.25
        12 0.25 0.09409 0.25
        12 0.5 0.21676 0.51068
        12 -0.25 -0.09409 -0.25
        14 0.25 0.65222 0.25
        16 0.5 0.11291 -0.12842
        12 0.5 -0.5 1.0
        14 0.5 -0.291 0.8787
        14 0.25 -0.65222 0.75
        14 0.5 0.291 0.1213
        16 0.0 0.11291 0.62842
        12 0.25 -0.09409 0.75
        14 0.5 0.43193 0.37613
        12 0.0 0.5 0.5
        14 0.0 -0.291 -0.3787
        12 0.0 0.21676 -0.01068
        16 0.0 -0.11291 -0.62842
        12 -0.5 -0.21676 -0.51068
        14 -0.25 0.65222 -0.75
        12 0.5 0.0 0.5
        14 0.0 -0.43193 -0.12387
        12 -0.25 0.09409 -0.75
        14 0.5 -0.43193 0.62387
        16 0.5 -0.11291 1.12842
        14 0.0 0.291 0.3787
        12 0.0 0.0 0.0
        """

        self.bondlen = 3

        self.cell = """
        13.167286191434481 31.492589961461622 18.629903136229707
        """

        self.density = 0.6190653349484135

        self.cell = cellvectors(a=13.167286191434481,
                                b=31.492589961461622,
                                c=18.629903136229707)
