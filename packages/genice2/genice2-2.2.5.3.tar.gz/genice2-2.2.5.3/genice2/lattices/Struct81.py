# coding: utf-8
"""
Data source: Dutour Sikirić, Mathieu, Olaf Delgado-Friedrichs, and Michel Deza. “Space Fullerenes: a Computer Search for New Frank-Kasper Structures” Acta Crystallographica Section A Foundations of Crystallography 66.Pt 5 (2010): 602–615.

Cage composition:
 (12,14,15,16) = (30,12,12,6,)
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
        126 23
        120 111
        165 30
        294 252
        147 26
        137 256
        321 32
        218 313
        205 25
        186 8
        164 139
        210 311
        169 142
        58 254
        129 89
        244 334
        250 166
        334 190
        4 341
        203 125
        77 81
        295 99
        195 223
        1 107
        59 168
        95 127
        208 239
        217 133
        87 224
        150 79
        176 82
        264 15
        191 44
        100 306
        265 300
        209 319
        275 40
        158 163
        207 194
        309 121
        180 22
        312 149
        116 331
        277 51
        48 318
        251 69
        169 321
        3 190
        337 296
        167 37
        130 146
        186 119
        64 159
        309 130
        283 235
        183 249
        261 296
        215 286
        198 48
        100 304
        226 34
        38 267
        230 1
        162 268
        253 310
        270 22
        168 294
        19 47
        208 117
        321 337
        188 290
        135 212
        90 45
        49 75
        284 83
        22 68
        199 80
        95 306
        60 304
        128 129
        21 20
        76 163
        282 23
        298 150
        157 314
        124 190
        79 103
        129 95
        170 322
        244 214
        323 149
        98 104
        63 132
        263 51
        133 175
        210 156
        298 245
        3 82
        2 204
        282 311
        288 280
        29 252
        108 117
        93 213
        177 17
        330 97
        113 248
        123 223
        17 115
        240 155
        301 180
        118 78
        249 278
        122 273
        209 11
        165 103
        332 65
        60 86
        233 183
        210 203
        314 109
        222 148
        267 139
        184 69
        151 294
        285 75
        85 108
        225 242
        323 41
        28 6
        157 50
        327 36
        278 22
        214 112
        43 122
        71 194
        115 49
        316 216
        102 136
        179 113
        148 39
        91 134
        196 108
        68 176
        181 94
        87 335
        57 283
        217 237
        268 115
        86 290
        162 178
        338 67
        80 175
        137 183
        93 165
        143 105
        203 229
        255 307
        330 319
        273 241
        234 70
        205 321
        137 134
        283 289
        145 173
        58 114
        196 331
        10 226
        4 105
        233 26
        143 78
        296 97
        148 277
        150 6
        295 8
        25 94
        7 325
        198 234
        332 307
        291 101
        215 17
        189 219
        247 35
        57 263
        185 228
        53 59
        90 336
        123 219
        28 213
        280 131
        225 338
        229 262
        327 189
        244 139
        27 216
        5 7
        339 302
        293 265
        305 308
        38 115
        292 107
        274 33
        315 277
        120 112
        333 56
        199 118
        205 341
        242 62
        3 270
        96 184
        326 335
        303 294
        297 258
        237 322
        282 40
        340 244
        152 160
        151 147
        160 326
        38 285
        276 47
        77 8
        243 268
        229 83
        171 18
        260 221
        53 316
        14 232
        215 207
        161 206
        202 287
        57 13
        2 200
        318 55
        194 317
        231 155
        63 306
        254 182
        127 55
        278 134
        153 234
        26 258
        128 149
        309 72
        331 219
        293 50
        212 176
        92 189
        196 230
        15 30
        173 168
        123 245
        312 318
        88 283
        88 284
        329 219
        188 131
        28 329
        222 4
        301 164
        44 338
        260 69
        130 214
        20 236
        66 235
        337 305
        62 106
        179 29
        340 111
        195 114
        174 263
        144 60
        53 135
        76 241
        21 159
        124 180
        96 21
        221 310
        211 30
        173 16
        200 241
        284 311
        113 147
        37 229
        62 114
        183 228
        6 106
        295 240
        187 142
        328 216
        24 23
        154 320
        313 306
        204 250
        227 107
        145 42
        177 243
        101 200
        295 184
        161 112
        330 322
        225 246
        182 117
        102 289
        308 252
        146 21
        146 70
        237 142
        84 106
        196 245
        12 43
        310 55
        73 278
        262 46
        301 71
        164 190
        59 26
        19 325
        324 264
        269 56
        10 300
        132 119
        313 280
        211 224
        54 153
        79 36
        213 230
        31 114
        91 185
        239 223
        143 282
        110 121
        63 41
        32 308
        191 36
        327 84
        215 14
        231 99
        208 245
        319 308
        96 206
        146 231
        170 133
        276 81
        101 226
        158 300
        257 118
        292 33
        12 10
        256 303
        216 68
        8 253
        271 14
        191 287
        78 341
        225 127
        24 174
        251 119
        134 172
        286 162
        227 264
        274 141
        266 220
        291 152
        336 300
        129 246
        92 238
        206 72
        177 339
        275 296
        85 238
        87 238
        11 29
        285 249
        93 108
        75 228
        19 338
        87 103
        292 61
        194 236
        297 328
        159 155
        2 46
        324 152
        7 192
        180 52
        248 185
        199 97
        193 251
        143 88
        250 43
        166 10
        202 290
        315 65
        250 241
        173 185
        261 39
        35 29
        154 9
        126 263
        123 202
        40 138
        231 72
        73 232
        13 9
        302 269
        207 38
        200 156
        100 131
        272 255
        330 25
        167 235
        144 63
        74 224
        144 149
        291 279
        240 121
        325 220
        260 132
        145 328
        240 18
        316 270
        316 271
        165 33
        192 323
        104 145
        118 174
        337 138
        188 47
        24 80
        293 279
        58 92
        13 277
        65 320
        260 234
        116 335
        208 220
        167 284
        96 121
        333 64
        39 341
        233 248
        150 230
        193 99
        37 201
        54 218
        83 320
        206 193
        175 320
        2 279
        28 327
        279 122
        148 275
        301 73
        56 155
        218 81
        53 82
        3 249
        137 258
        7 131
        288 221
        120 269
        9 289
        56 110
        170 199
        113 16
        169 97
        317 110
        315 40
        179 181
        5 67
        135 14
        340 317
        192 288
        61 211
        59 328
        128 86
        105 126
        141 74
        276 310
        116 61
        158 109
        5 242
        95 312
        201 125
        161 159
        299 235
        94 32
        144 81
        292 213
        313 119
        297 172
        12 293
        98 247
        11 94
        45 160
        24 83
        33 335
        128 62
        191 117
        256 42
        85 211
        299 34
        141 30
        265 152
        125 34
        102 299
        201 0
        198 186
        281 259
        77 132
        157 0
        27 49
        171 186
        261 25
        204 50
        207 73
        136 307
        85 254
        203 23
        100 89
        201 66
        257 142
        90 76
        192 318
        91 232
        60 47
        107 224
        171 193
        78 138
        84 44
        90 166
        157 166
        259 273
        336 324
        167 156
        86 31
        140 256
        270 178
        286 339
        210 46
        182 31
        218 312
        140 168
        169 209
        326 264
        1 15
        332 13
        254 329
        217 51
        109 227
        265 314
        58 6
        184 70
        198 288
        187 11
        98 16
        314 45
        281 109
        27 42
        255 57
        151 181
        197 139
        12 299
        151 319
        20 110
        42 228
        266 106
        170 138
        124 176
        66 50
        48 253
        246 195
        27 212
        154 136
        276 280
        223 89
        247 147
        124 177
        111 52
        268 333
        281 76
        101 163
        68 172
        130 18
        238 331
        257 39
        35 258
        247 209
        205 237
        236 64
        332 46
        302 214
        179 297
        116 15
        140 135
        324 281
        336 141
        69 253
        298 266
        311 65
        182 202
        74 326
        163 160
        162 271
        158 74
        197 112
        17 212
        171 70
        232 75
        329 61
        248 172
        289 105
        67 287
        19 55
        41 127
        156 34
        323 242
        305 187
        41 221
        204 307
        309 340
        233 82
        71 111
        104 303
        93 36
        103 1
        52 178
        45 274
        226 0
        92 79
        243 269
        271 49
        339 334
        188 67
        222 175
        104 181
        285 164
        333 267
        37 273
        298 287
        153 99
        305 322
        255 66
        189 195
        140 91
        5 266
        304 239
        16 252
        315 133
        88 174
        267 317
        20 302
        77 153
        54 48
        154 262
        220 44
        54 251
        222 9
        261 187
        259 0
        178 334
        243 52
        291 259
        272 125
        197 64
        272 126
        89 290
        257 51
        275 80
        272 102
        122 262
        35 303
        98 32
        18 161
        246 84
        31 239
        274 227
        120 72
        325 304
        286 236
        43 136
        217 4
        197 71
        """

        self.waters = """
        0.875 0.5 0.08449
        0.58491 0.29245 0.21055
        0.97491 0.0748 0.05339
        0.73633 0.43067 0.68111
        0.3217 0.76836 0.93174
        0.56933 0.30566 0.34777
        0.59991 0.52511 0.28005
        0.7409 0.38407 0.37607
        0.125 0.625 0.47227
        0.57168 0.89336 0.97889
        0.2751 0.67521 0.09556
        0.75 0.75 0.83333
        0.44667 0.76836 0.06825
        0.82168 0.89336 0.97889
        0.2633 0.19414 0.68111
        0.625 0.125 0.19439
        0.08255 0.29245 0.79343
        0.35664 0.92832 0.65888
        0.875 0.375 0.52384
        0.11571 0.75926 0.37607
        0.3248 0.09991 0.57099
        0.29246 0.20991 0.54377
        0.7367 0.80586 0.68111
        0.95342 0.40685 0.9717
        0.7409 0.35683 0.95725
        0.5 0.875 0.85718
        0.67521 0.40011 0.76223
        0.35683 0.7409 0.70941
        0.77148 0.72853 0.26109
        0.875 0.875 0.80959
        0.375 0.875 0.19439
        0.30566 0.56933 0.31889
        0.25 0.5 0.83333
        0.0 0.875 0.19041
        0.18741 0.49982 0.05052
        0.91746 0.70755 0.79343
        0.17834 0.9467 0.26497
        0.61593 0.35683 0.04274
        0.10664 0.67832 0.64556
        0.65011 0.80021 0.90045
        0.05331 0.23164 0.93163
        0.27148 0.22853 0.40557
        0.23164 0.67831 0.73492
        0.4001 0.92521 0.05328
        0.06916 0.80586 0.31889
        0.0 0.875 0.14293
        0.92832 0.10664 0.02111
        0.31241 0.81259 0.38385
        0.83255 0.66509 0.44777
        0.26367 0.56933 0.68111
        0.82167 0.76836 0.06836
        0.9467 0.76836 0.93163
        0.64355 0.75926 0.62392
        0.49982 0.31241 0.71719
        0.70755 0.79009 0.4601
        0.05331 0.82167 0.40169
        0.3248 0.72491 0.5711
        0.80586 0.7367 0.98555
        0.4001 0.47489 0.28005
        0.5 0.375 0.75116
        0.2591 0.61593 0.37607
        0.66509 0.83255 0.21889
        0.5 0.5 0.33333
        0.17159 0.32843 0.41276
        0.15685 0.32843 0.58723
        0.17832 0.10664 0.97889
        0.75926 0.64355 0.04274
        0.42832 0.07168 0.34111
        0.64355 0.88429 0.70941
        0.125 0.0 0.47626
        0.5 0.25 0.49999
        0.92521 0.0251 0.61327
        0.70755 0.79009 0.54377
        0.0 0.0 0.66666
        0.25 0.5 0.16667
        0.10664 0.42832 0.68777
        0.33491 0.16746 0.11444
        0.29245 0.58491 0.45612
        0.375 0.5 0.9155
        0.32843 0.17159 0.2539
        0.67831 0.23164 0.93174
        0.40011 0.72491 0.42889
        0.64318 0.2591 0.70941
        0.56933 0.26367 0.98555
        0.92832 0.82168 0.31223
        0.2751 0.59989 0.23777
        0.43067 0.69434 0.34777
        0.20991 0.29245 0.20656
        0.5 0.5 0.97111
        0.80586 0.06916 0.34777
        0.20991 0.91746 0.12677
        0.0748 0.09989 0.72005
        0.22853 0.27148 0.26109
        0.09991 0.77511 0.23766
        0.5 0.75 0.83333
        0.90011 0.97491 0.38672
        0.125 0.0 0.52374
        0.70755 0.29246 0.87722
        0.125 0.5 0.80948
        0.5 0.75 0.49999
        0.88429 0.24074 0.37607
        0.09991 0.3248 0.09567
        0.30566 0.73633 0.01444
        0.33491 0.16745 0.21889
        0.29246 0.70755 0.78945
        0.2591 0.64318 0.95725
        0.67832 0.57168 0.31223
        0.625 0.5 0.19051
        0.125 0.625 0.24884
        0.625 0.5 0.13894
        0.1998 0.84991 0.56712
        0.76836 0.82167 0.5983
        0.80021 0.1501 0.56712
        0.83255 0.16745 0.7811
        0.32168 0.42832 0.31223
        0.26367 0.69434 0.65222
        0.79009 0.08255 0.21044
        0.18741 0.68759 0.28281
        0.625 0.5 0.9155
        0.91745 0.20991 0.45623
        0.67521 0.9001 0.57099
        0.08255 0.79009 0.53989
        0.59991 0.0748 0.05328
        0.75926 0.11571 0.29059
        0.64336 0.07168 0.65888
        0.0 0.5 0.02889
        0.04659 0.59316 0.9717
        0.09989 0.0251 0.38672
        0.57168 0.67832 0.35444
        0.82168 0.92832 0.35444
        0.70755 0.41509 0.54388
        0.68759 0.18741 0.38385
        0.16745 0.33491 0.44777
        0.27148 0.04295 0.92776
        0.92521 0.90011 0.72005
        0.35646 0.11571 0.70941
        0.32168 0.89336 0.02111
        0.95705 0.72853 0.7389
        0.22489 0.3248 0.90432
        0.92521 0.4001 0.61338
        0.23164 0.05331 0.73503
        0.25 0.75 0.16667
        0.91745 0.70755 0.87711
        0.31241 0.49982 0.94947
        0.3217 0.55334 0.40158
        0.3248 0.59989 0.76223
        0.5 0.375 0.52772
        0.70755 0.29245 0.78945
        0.72853 0.95705 0.92776
        0.52511 0.59991 0.38661
        0.55334 0.3217 0.26508
        0.5 0.125 0.8056
        0.79009 0.08255 0.12677
        0.5 0.625 0.47615
        0.5 0.0 0.0
        0.29246 0.58491 0.54388
        0.24074 0.35646 0.04274
        0.9001 0.67521 0.09567
        0.375 0.5 0.13894
        0.16746 0.33491 0.55222
        0.0 0.125 0.14293
        0.91746 0.20991 0.53989
        0.40685 0.45343 0.63836
        0.20991 0.29246 0.1229
        0.89336 0.32168 0.64556
        0.20991 0.91745 0.21044
        0.1501 0.80021 0.09955
        0.45343 0.40685 0.0283
        0.3248 0.22489 0.76234
        0.875 0.5 0.86106
        0.34989 0.1998 0.90045
        0.75 0.25 0.5
        0.76836 0.9467 0.73503
        0.1998 0.34989 0.76621
        0.68759 0.50019 0.94947
        0.47489 0.0748 0.94672
        0.59316 0.04659 0.69496
        0.5 0.0 0.63778
        0.59316 0.54657 0.63836
        0.70755 0.91745 0.78956
        0.7367 0.93084 0.65222
        0.5 0.875 0.8056
        0.38407 0.7409 0.29059
        0.92521 0.52511 0.71994
        0.25 0.0 0.5
        0.04295 0.27148 0.7389
        0.875 0.375 0.47227
        0.875 0.875 0.85707
        0.5 0.0 0.36222
        0.0251 0.09989 0.27994
        0.73633 0.30566 0.65222
        0.24074 0.88429 0.29059
        0.67831 0.44667 0.40158
        0.75 0.0 0.5
        0.0748 0.97491 0.61327
        0.07168 0.17832 0.31223
        0.875 0.375 0.24884
        0.95705 0.22853 0.59442
        0.70755 0.41509 0.45612
        0.59989 0.3248 0.90443
        0.17834 0.23164 0.06836
        0.81259 0.50019 0.05052
        0.54657 0.95342 0.30503
        0.92832 0.35664 0.00778
        0.0251 0.92521 0.05339
        0.29245 0.70755 0.87722
        0.875 0.0 0.52374
        0.10664 0.92832 0.64556
        0.0 0.5 0.30445
        0.75 0.5 0.83333
        0.06916 0.2633 0.01444
        0.41509 0.70755 0.21055
        0.40685 0.95342 0.69496
        0.84991 0.65011 0.23379
        0.67521 0.2751 0.5711
        0.2633 0.06916 0.65222
        0.50019 0.68759 0.71719
        0.17159 0.84316 0.92057
        0.65011 0.84991 0.43288
        0.82167 0.05331 0.26497
        0.92832 0.57168 0.32555
        0.34989 0.1501 0.43288
        0.52511 0.92521 0.94672
        0.93084 0.19414 0.31889
        0.375 0.5 0.19051
        0.17832 0.07168 0.35444
        0.125 0.5 0.08449
        0.75 0.5 0.16667
        0.0748 0.47489 0.71994
        0.69434 0.26367 0.01444
        0.72491 0.40011 0.23777
        0.5 0.625 0.52772
        0.10664 0.17832 0.68777
        0.76836 0.3217 0.73492
        0.5 0.375 0.47615
        0.54657 0.59316 0.0283
        0.23164 0.17834 0.5983
        0.16745 0.83255 0.88556
        0.1501 0.34989 0.23379
        0.07168 0.42832 0.32555
        0.125 0.625 0.52384
        0.32843 0.15685 0.07943
        0.42832 0.32168 0.35444
        0.50019 0.81259 0.61614
        0.76836 0.44667 0.59841
        0.81259 0.31241 0.28281
        0.0 0.0 0.33333
        0.875 0.5 0.80948
        0.84316 0.17159 0.74609
        0.89336 0.57168 0.68777
        0.22853 0.95705 0.07224
        0.875 0.0 0.47626
        0.125 0.125 0.80959
        0.08255 0.79009 0.45623
        0.44667 0.67831 0.26508
        0.93084 0.7367 0.01444
        0.15685 0.82842 0.74609
        0.77511 0.67521 0.90432
        0.80021 0.65011 0.76621
        0.72491 0.3248 0.09556
        0.29245 0.20991 0.4601
        0.70755 0.91746 0.87323
        0.67832 0.10664 0.02111
        0.88429 0.64355 0.95725
        0.75 0.25 0.16667
        0.66509 0.83255 0.11444
        0.69434 0.43067 0.31889
        0.0748 0.59991 0.61338
        0.35683 0.61593 0.62392
        0.5 0.875 0.58217
        0.64336 0.57168 0.67445
        0.35664 0.42832 0.67445
        0.07168 0.64336 0.00778
        0.55334 0.23164 0.06825
        0.0 0.75 0.16667
        0.82842 0.15685 0.92057
        0.375 0.875 0.41782
        0.90011 0.92521 0.94661
        0.89336 0.82168 0.68777
        0.77148 0.04295 0.07224
        0.625 0.125 0.41782
        0.58491 0.29246 0.12279
        0.11571 0.35646 0.95725
        0.57168 0.64336 0.99221
        0.42832 0.35664 0.99221
        0.0 0.5 0.66666
        0.35646 0.24074 0.62392
        0.45343 0.04659 0.30503
        0.59989 0.2751 0.42889
        0.43067 0.73633 0.98555
        0.57168 0.92832 0.34111
        0.84991 0.1998 0.09955
        0.79009 0.70755 0.20656
        0.67157 0.84316 0.07943
        0.29246 0.08255 0.78956
        0.25 0.75 0.5
        0.83255 0.16746 0.88556
        0.67521 0.77511 0.76234
        0.61593 0.2591 0.29059
        0.38407 0.64318 0.04274
        0.41509 0.70755 0.12279
        0.89336 0.07168 0.64556
        0.5 0.125 0.58217
        0.16746 0.83255 0.7811
        0.04659 0.45343 0.36163
        0.125 0.125 0.85707
        0.9467 0.17834 0.40169
        0.07168 0.89336 0.02111
        0.25 0.25 0.83333
        0.83255 0.66509 0.55222
        0.22489 0.9001 0.429
        0.19414 0.2633 0.98555
        0.72853 0.77148 0.40557
        0.77511 0.09991 0.429
        0.79009 0.70755 0.1229
        0.09989 0.0748 0.94661
        0.5 0.5 0.69556
        0.04295 0.77148 0.59442
        0.82842 0.67157 0.41276
        0.5 0.25 0.83333
        0.42832 0.10664 0.97889
        0.125 0.5 0.86106
        0.29245 0.08255 0.87323
        0.47489 0.4001 0.38661
        0.625 0.125 0.14282
        0.95342 0.54657 0.36163
        0.0 0.25 0.16667
        0.97491 0.90011 0.27994
        0.5 0.625 0.75116
        0.67157 0.82842 0.2539
        0.5 0.125 0.85718
        0.9001 0.22489 0.23766
        0.0 0.0 0.0
        0.23164 0.55334 0.59841
        0.64318 0.38407 0.62392
        0.0 0.125 0.19041
        0.375 0.875 0.14282
        0.08255 0.29246 0.87711
        0.19414 0.93084 0.34777
        0.49982 0.18741 0.61614
        0.84316 0.67157 0.58723
        0.40011 0.67521 0.90443
        """

        self.coord = "relative"

        self.cages = """
        12 0.10038 0.39956 0.27556
        12 0.60044 0.70082 0.94222
        12 0.89962 0.60044 0.27556
        12 0.39956 0.10038 0.3911
        12 0.29918 0.89962 0.60889
        12 0.39956 0.29918 0.94222
        12 0.70082 0.60044 0.72444
        12 0.60044 0.89962 0.3911
        12 0.89962 0.29918 0.05777
        12 0.70082 0.10038 0.60889
        12 0.29918 0.39956 0.72444
        12 0.10038 0.70082 0.05777
        12 0.5 0.0 0.10205
        12 0.0 0.5 0.76871
        12 0.0 0.5 0.56461
        12 0.5 0.5 0.43538
        12 0.5 0.0 0.89795
        12 0.5 0.5 0.23128
        12 0.24963 0.49926 0.0
        12 0.50074 0.75037 0.66666
        12 0.75037 0.50074 0.0
        12 0.49926 0.24963 0.66666
        12 0.24963 0.75037 0.33333
        12 0.75037 0.24963 0.33333
        15 0.0 0.5 0.13588
        15 0.5 0.5 0.80254
        15 0.5 0.0 0.53078
        15 0.5 0.0 0.46921
        15 0.5 0.5 0.86412
        15 0.0 0.5 0.19745
        12 0.0 0.0 0.10249
        12 0.0 0.0 0.76915
        12 0.0 0.0 0.56417
        12 0.0 0.0 0.43582
        12 0.0 0.0 0.89751
        12 0.0 0.0 0.23084
        15 0.33963 0.16982 0.16667
        15 0.83018 0.16981 0.83333
        15 0.66037 0.83018 0.16667
        15 0.16982 0.33963 0.49999
        15 0.83019 0.66037 0.5
        15 0.16982 0.83019 0.83333
        14 0.31372 0.12738 0.02665
        14 0.87262 0.18634 0.69331
        14 0.68628 0.87262 0.02665
        14 0.12738 0.31372 0.64001
        14 0.81366 0.68628 0.35998
        14 0.12738 0.81366 0.69331
        14 0.18634 0.87262 0.97335
        14 0.87262 0.68628 0.64001
        14 0.68628 0.81366 0.30668
        14 0.18634 0.31372 0.35998
        14 0.81366 0.12738 0.97335
        14 0.31372 0.18634 0.30668
        16 0.5 0.0 0.24679
        16 0.0 0.5 0.91345
        16 0.0 0.5 0.41987
        16 0.5 0.5 0.58012
        16 0.5 0.0 0.75321
        16 0.5 0.5 0.08654
        """

        self.bondlen = 3

        self.cell = """
        17.755155395905042 0.0 0.0
        -8.877577697952516 15.37641562099412 0.0
        7.0208249310484485e-15 1.2160425491622169e-14 114.65877240583357
        """

        self.density = 0.3265660139261983

        self.cell = cellvectors(a=17.755155395905042,
                                b=17.75515539590504,
                                c=114.65877240583357,
                                C=119.99999999999999)
