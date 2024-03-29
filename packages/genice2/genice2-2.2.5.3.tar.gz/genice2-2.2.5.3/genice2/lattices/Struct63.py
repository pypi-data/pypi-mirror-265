# coding: utf-8
"""
Data source: Dutour Sikirić, Mathieu, Olaf Delgado-Friedrichs, and Michel Deza. “Space Fullerenes: a Computer Search for New Frank-Kasper Structures” Acta Crystallographica Section A Foundations of Crystallography 66.Pt 5 (2010): 602–615.

Cage composition:
 (12,14,15,16) = (12,16,8,0,)
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
        179 160
        1 168
        66 30
        159 66
        17 104
        170 70
        69 64
        63 101
        97 21
        35 186
        13 137
        205 192
        3 92
        151 59
        91 113
        123 192
        130 111
        100 106
        92 205
        173 101
        13 160
        33 57
        111 82
        141 110
        194 175
        118 68
        86 4
        190 120
        47 198
        88 31
        126 199
        11 29
        56 29
        168 109
        167 168
        150 151
        137 39
        60 26
        167 93
        10 192
        51 88
        141 80
        59 205
        164 3
        28 99
        25 106
        111 178
        8 81
        105 129
        189 102
        183 132
        152 102
        8 157
        127 81
        79 84
        112 127
        60 129
        37 81
        93 128
        191 73
        116 194
        107 92
        142 187
        178 113
        83 185
        66 59
        145 95
        164 26
        43 82
        2 137
        37 166
        149 56
        76 89
        5 130
        31 93
        138 50
        195 7
        167 6
        207 196
        157 140
        2 107
        58 89
        15 143
        30 126
        119 20
        73 94
        30 166
        172 193
        142 204
        23 82
        150 202
        74 175
        28 101
        43 19
        161 34
        35 155
        147 12
        125 41
        80 50
        49 102
        36 116
        163 17
        102 34
        112 59
        37 152
        171 175
        177 191
        18 120
        71 144
        98 61
        172 148
        91 115
        13 166
        134 176
        51 132
        156 93
        122 138
        165 176
        58 5
        48 157
        19 158
        36 40
        20 175
        141 11
        86 7
        28 130
        150 83
        72 122
        121 201
        45 78
        21 94
        36 74
        5 204
        0 77
        135 43
        112 179
        130 68
        23 173
        203 147
        12 32
        129 144
        140 126
        67 186
        124 18
        162 94
        204 101
        146 206
        131 99
        137 136
        10 9
        87 40
        140 162
        0 46
        131 168
        76 7
        196 181
        57 91
        133 29
        36 3
        35 120
        133 104
        161 138
        138 160
        55 154
        47 44
        100 199
        24 160
        190 109
        142 104
        17 195
        85 186
        53 46
        95 206
        53 177
        90 38
        112 166
        48 16
        79 198
        171 17
        14 203
        19 198
        110 26
        103 185
        71 20
        13 34
        197 156
        18 85
        159 103
        64 125
        46 11
        170 105
        91 121
        207 136
        33 165
        55 106
        115 129
        170 4
        127 39
        183 197
        148 133
        62 139
        53 90
        50 38
        117 27
        111 158
        173 108
        149 184
        67 97
        191 38
        24 136
        98 176
        174 45
        163 89
        54 109
        113 12
        131 65
        52 143
        61 115
        110 171
        78 188
        97 199
        204 117
        2 169
        169 140
        132 154
        8 52
        57 62
        88 6
        135 15
        44 125
        95 176
        174 191
        38 9
        146 154
        58 104
        194 56
        174 161
        114 76
        49 128
        123 77
        74 144
        73 199
        155 97
        24 80
        62 201
        48 143
        145 203
        198 147
        71 61
        80 149
        39 78
        154 189
        58 86
        156 188
        162 192
        77 9
        180 122
        55 64
        37 42
        193 151
        57 98
        151 153
        61 32
        183 125
        25 189
        202 172
        67 84
        180 200
        33 147
        46 122
        12 158
        72 45
        165 51
        201 195
        187 4
        190 52
        75 6
        150 159
        127 169
        202 4
        146 128
        116 185
        180 39
        193 181
        8 155
        81 188
        22 121
        87 70
        173 76
        110 184
        34 78
        65 19
        65 15
        149 148
        18 43
        5 170
        124 99
        159 107
        62 163
        197 45
        1 118
        84 44
        70 144
        152 156
        49 52
        28 1
        1 108
        14 64
        206 51
        96 139
        181 133
        73 10
        134 203
        100 162
        0 56
        42 155
        124 32
        44 21
        86 148
        136 200
        135 75
        66 10
        41 106
        178 27
        182 108
        0 50
        177 100
        95 182
        2 30
        167 15
        82 63
        23 75
        22 60
        201 114
        42 48
        119 98
        63 27
        54 206
        202 207
        114 182
        169 205
        103 164
        178 70
        99 158
        92 153
        116 77
        60 185
        35 16
        24 172
        197 189
        22 184
        153 40
        49 188
        180 179
        96 88
        183 31
        128 109
        27 115
        42 126
        26 74
        179 193
        14 47
        157 21
        142 7
        164 90
        123 3
        118 6
        145 96
        85 79
        25 161
        196 187
        22 194
        165 79
        139 182
        40 83
        131 120
        87 187
        200 11
        65 16
        174 41
        196 153
        119 163
        71 113
        103 9
        54 75
        33 96
        141 90
        134 85
        47 16
        190 135
        14 186
        152 143
        53 123
        118 139
        171 29
        83 105
        124 63
        87 117
        68 89
        23 68
        105 117
        134 32
        55 67
        25 72
        184 195
        200 181
        84 132
        119 114
        94 41
        107 207
        72 177
        146 69
        145 69
        69 31
        54 108
        121 20
        """

        self.waters = """
        0.3125 0.1875 0.5106
        0.84556 0.85799 0.07197
        0.32303 0.67165 0.6064
        0.38603 0.43685 0.48829
        0.375 0.75 0.34511
        0.625 0.75 0.24476
        0.61397 0.93685 0.01171
        0.13915 0.92165 0.28041
        0.98109 0.65786 0.79493
        0.937 0.35981 0.5486
        0.91859 0.43867 0.60885
        0.76103 0.06185 0.48829
        0.33141 0.43867 0.10885
        0.32038 0.87449 0.64323
        0.34556 0.35799 0.92803
        0.42647 0.74935 0.92513
        0.41859 0.56133 0.89115
        0.76415 0.04665 0.29203
        0.88603 0.56316 0.01171
        0.23897 0.56185 0.01171
        0.375 0.25 0.25525
        0.01415 0.45335 0.79203
        0.05147 0.25066 0.33451
        0.32303 0.82835 0.1064
        0.23897 0.93816 0.51171
        0.43388 0.125 0.72734
        0.67698 0.32835 0.3936
        0.98585 0.54665 0.20797
        0.75 0.75 0.12052
        0.61712 0.06301 0.41346
        0.53256 0.62682 0.64323
        0.88288 0.06301 0.91346
        0.58141 0.43867 0.10885
        0.92647 0.24935 0.07488
        0.23585 0.95335 0.70797
        0.66859 0.56133 0.89115
        0.27994 0.43568 0.41346
        0.625 0.75 0.74476
        0.92647 0.25066 0.57488
        0.96744 0.87318 0.64323
        0.08141 0.56133 0.39115
        0.125 0.25 0.75525
        0.56613 0.625 0.77267
        0.125 0.625 0.02343
        0.03256 0.37318 0.85677
        0.86085 0.07835 0.71959
        0.56301 0.14019 0.5486
        0.22006 0.43568 0.91346
        0.35609 0.62383 0.82284
        0.14391 0.87617 0.82284
        0.16595 0.1415 0.5486
        0.625 0.125 0.97658
        0.125 0.75 0.84511
        0.57353 0.24935 0.57488
        0.26103 0.93816 0.01171
        0.44853 0.25066 0.83451
        0.34556 0.14202 0.42803
        0.875 0.25 0.1549
        0.56613 0.875 0.27267
        0.84556 0.64202 0.57197
        0.82038 0.37449 0.35677
        0.64391 0.37617 0.17716
        0.85609 0.12383 0.17716
        0.96744 0.62682 0.14323
        0.25 0.25 0.87949
        0.437 0.64019 0.95141
        0.72006 0.56432 0.58654
        0.67962 0.37449 0.85677
        0.53256 0.87318 0.14323
        0.15444 0.14202 0.92803
        0.36085 0.57835 0.28041
        0.43388 0.375 0.22734
        0.64391 0.12383 0.67716
        0.85609 0.37617 0.67716
        0.46744 0.37318 0.35677
        0.375 0.875 0.02343
        0.26415 0.95335 0.20797
        0.1875 0.3125 0.5106
        0.98585 0.95335 0.70797
        0.875 0.375 0.97658
        0.11397 0.06316 0.48829
        0.875 0.75 0.74476
        0.17698 0.67165 0.1064
        0.83141 0.56133 0.39115
        0.82303 0.32835 0.8936
        0.76103 0.43816 0.98829
        0.35609 0.87617 0.32284
        0.14391 0.62383 0.32284
        0.73897 0.06185 0.98829
        0.51415 0.95335 0.20797
        0.75 0.25 0.52914
        0.01891 0.34214 0.20507
        0.26103 0.56185 0.51171
        0.83141 0.93867 0.89115
        0.06613 0.375 0.72734
        0.33406 0.1415 0.0486
        0.937 0.14019 0.0486
        0.76415 0.45335 0.79203
        0.625 0.25 0.1549
        0.65444 0.64202 0.07197
        0.48109 0.34214 0.70507
        0.94853 0.75066 0.1655
        0.36085 0.92165 0.78041
        0.73897 0.43816 0.48829
        0.76415 0.92165 0.31469
        0.73585 0.57835 0.31469
        0.375 0.25 0.75525
        0.375 0.625 0.52343
        0.11712 0.93699 0.08654
        0.06301 0.85981 0.95141
        0.82303 0.17165 0.3936
        0.32038 0.62551 0.14323
        0.75 0.75 0.62052
        0.23585 0.42165 0.18531
        0.26415 0.07835 0.18531
        0.86085 0.42165 0.21959
        0.15444 0.35799 0.42803
        0.93388 0.625 0.27267
        0.72006 0.93568 0.08654
        0.48109 0.15786 0.20507
        0.83406 0.6415 0.95141
        0.125 0.25 0.25525
        0.58141 0.06133 0.60885
        0.33406 0.3585 0.5486
        0.77994 0.56432 0.08654
        0.05147 0.24935 0.83451
        0.51415 0.54665 0.70797
        0.94853 0.74935 0.6655
        0.08141 0.93867 0.89115
        0.73585 0.45335 0.29203
        0.55147 0.74935 0.1655
        0.6875 0.6875 0.9894
        0.67698 0.17165 0.8936
        0.66859 0.93867 0.39115
        0.56301 0.35981 0.0486
        0.25 0.75 0.97087
        0.125 0.875 0.52343
        0.17698 0.82835 0.6064
        0.33141 0.06133 0.60885
        0.91859 0.06133 0.10885
        0.26415 0.54665 0.70797
        0.875 0.125 0.47658
        0.98109 0.84214 0.29493
        0.375 0.75 0.84511
        0.48585 0.45335 0.29203
        0.1875 0.1875 0.0106
        0.27994 0.06432 0.91346
        0.16595 0.3585 0.0486
        0.41859 0.93867 0.39115
        0.22006 0.06432 0.41346
        0.66595 0.6415 0.45141
        0.8125 0.6875 0.4894
        0.51891 0.84214 0.79493
        0.06301 0.64019 0.45141
        0.46744 0.12682 0.85677
        0.76415 0.57835 0.81469
        0.73585 0.92165 0.81469
        0.13915 0.57835 0.78041
        0.38288 0.56301 0.08654
        0.61397 0.56316 0.51171
        0.38288 0.93699 0.58654
        0.23585 0.07835 0.68531
        0.26415 0.42165 0.68531
        0.63915 0.07835 0.21959
        0.625 0.375 0.47658
        0.75 0.25 0.02914
        0.55147 0.75066 0.6655
        0.66595 0.8585 0.95141
        0.8125 0.8125 0.9894
        0.17962 0.62551 0.64323
        0.51891 0.65786 0.29493
        0.67962 0.12551 0.35677
        0.437 0.85981 0.45141
        0.17962 0.87449 0.14323
        0.01891 0.15786 0.70507
        0.44853 0.24935 0.33451
        0.57353 0.25066 0.07488
        0.625 0.25 0.6549
        0.23585 0.54665 0.20797
        0.65444 0.85799 0.57197
        0.77994 0.93568 0.58654
        0.83406 0.8585 0.45141
        0.16859 0.06133 0.10885
        0.82038 0.12551 0.85677
        0.03256 0.12682 0.35677
        0.88288 0.43699 0.41346
        0.61712 0.43699 0.91346
        0.125 0.75 0.34511
        0.93388 0.875 0.77267
        0.48585 0.04665 0.79203
        0.07353 0.75066 0.92513
        0.875 0.25 0.6549
        0.16859 0.43867 0.60885
        0.6875 0.8125 0.4894
        0.25 0.25 0.37949
        0.01415 0.04665 0.29203
        0.07353 0.74935 0.42513
        0.73585 0.04665 0.79203
        0.11397 0.43685 0.98829
        0.63915 0.42165 0.71959
        0.88603 0.93685 0.51171
        0.06613 0.125 0.22734
        0.42647 0.75066 0.42513
        0.3125 0.3125 0.0106
        0.875 0.75 0.24476
        0.11712 0.56301 0.58654
        0.38603 0.06316 0.98829
        0.25 0.75 0.47087
        """

        self.coord = "relative"

        self.cages = """
        12 0.54412 0.24738 0.45315
        12 0.95588 0.25262 0.45315
        12 0.45588 0.74738 0.04685
        12 0.45588 0.75262 0.54685
        12 0.04412 0.75262 0.04685
        12 0.04412 0.74738 0.54685
        12 0.54412 0.25262 0.95315
        12 0.95588 0.24738 0.95315
        14 0.25 0.25 0.13611
        14 0.75 0.75 0.36389
        14 0.75 0.75 0.86389
        14 0.25 0.25 0.63611
        14 0.38225 0.06806 0.30582
        14 0.11775 0.43194 0.30582
        14 0.61775 0.56806 0.19418
        14 0.61775 0.93194 0.69418
        14 0.88225 0.93194 0.19418
        14 0.88225 0.56806 0.69418
        14 0.38225 0.43194 0.80582
        14 0.11775 0.06806 0.80582
        15 0.5421 0.06339 0.10512
        15 0.9579 0.43661 0.10512
        15 0.4579 0.56339 0.39488
        15 0.4579 0.93661 0.89488
        15 0.0421 0.93661 0.39488
        15 0.0421 0.56339 0.89488
        15 0.5421 0.43661 0.60512
        15 0.9579 0.06339 0.60512
        12 0.0 0.0 0.0
        12 0.5 0.5 0.0
        12 0.0 0.5 0.5
        12 0.5 0.0 0.5
        14 0.25 0.75 0.22677
        14 0.75 0.25 0.27323
        14 0.75 0.25 0.77323
        14 0.25 0.75 0.72677
        """

        self.bondlen = 3

        self.cell = """
        16.097405686270985 30.870809118877812 57.365438878590446
        """

        self.density = 0.21809256820530465

        self.cell = cellvectors(a=16.097405686270985,
                                b=30.870809118877812,
                                c=57.365438878590446)
