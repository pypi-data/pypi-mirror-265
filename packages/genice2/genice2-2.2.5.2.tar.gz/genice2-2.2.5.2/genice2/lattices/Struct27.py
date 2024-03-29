# coding: utf-8
"""
Data source: Dutour Sikirić, Mathieu, Olaf Delgado-Friedrichs, and Michel Deza. “Space Fullerenes: a Computer Search for New Frank-Kasper Structures” Acta Crystallographica Section A Foundations of Crystallography 66.Pt 5 (2010): 602–615.

Cage composition:
 (12,14,15,16) = (33,6,6,12,)
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
        253 286
        217 233
        212 123
        162 282
        296 117
        268 276
        197 166
        174 139
        178 302
        19 180
        271 254
        270 126
        217 191
        156 231
        319 157
        28 22
        172 137
        161 289
        272 230
        158 102
        289 320
        216 278
        264 314
        14 240
        208 10
        0 41
        204 27
        122 250
        107 238
        260 134
        261 136
        215 78
        59 273
        51 21
        104 123
        82 168
        260 80
        147 226
        297 187
        122 169
        188 192
        294 52
        315 143
        223 296
        240 187
        238 21
        31 0
        38 221
        242 166
        321 158
        161 227
        304 184
        15 83
        316 211
        290 11
        81 127
        225 210
        30 13
        86 297
        9 303
        277 267
        264 202
        255 275
        131 284
        199 170
        64 139
        161 113
        11 89
        39 268
        37 36
        206 207
        122 256
        10 200
        66 289
        38 259
        246 250
        264 144
        310 166
        188 153
        26 30
        301 279
        203 17
        279 261
        64 120
        264 32
        323 295
        253 307
        41 247
        36 83
        4 114
        220 193
        292 168
        172 47
        107 40
        47 119
        56 128
        265 191
        3 256
        23 16
        279 29
        169 235
        251 50
        185 311
        29 229
        197 281
        189 316
        19 152
        178 149
        94 35
        283 80
        223 16
        243 298
        308 114
        134 184
        83 48
        34 312
        171 284
        91 154
        54 219
        129 269
        170 233
        88 212
        33 177
        320 35
        59 53
        132 288
        95 304
        195 42
        165 287
        174 10
        175 12
        268 201
        33 139
        252 288
        26 79
        299 162
        100 157
        68 82
        63 291
        199 213
        149 7
        218 303
        68 155
        60 89
        163 283
        130 6
        207 139
        290 97
        243 257
        92 249
        24 160
        186 108
        3 296
        34 121
        5 116
        78 114
        308 181
        266 162
        183 262
        145 179
        87 284
        60 289
        154 200
        20 90
        26 108
        178 266
        96 116
        212 179
        212 180
        70 121
        131 65
        79 32
        217 215
        299 21
        250 27
        56 143
        170 68
        255 13
        72 97
        172 226
        205 85
        219 262
        223 285
        143 168
        280 2
        197 7
        177 28
        183 244
        87 125
        316 113
        240 208
        67 263
        239 134
        224 162
        281 17
        244 53
        100 306
        95 228
        39 173
        273 257
        123 209
        51 282
        4 56
        148 220
        211 84
        309 262
        124 306
        258 93
        261 286
        118 88
        164 51
        205 248
        194 132
        45 220
        277 237
        122 106
        10 120
        226 234
        197 51
        96 127
        193 92
        196 91
        283 83
        270 319
        62 239
        140 313
        163 124
        216 148
        3 27
        201 84
        164 291
        110 237
        76 249
        7 176
        104 109
        161 267
        171 263
        198 113
        214 44
        295 135
        146 308
        205 34
        133 306
        69 92
        174 91
        258 274
        133 269
        164 77
        178 69
        58 192
        147 71
        294 216
        106 167
        236 158
        229 251
        136 323
        54 150
        209 18
        211 294
        132 286
        37 131
        288 136
        245 215
        118 170
        24 140
        190 13
        198 39
        121 6
        70 117
        305 77
        321 223
        90 214
        318 23
        199 181
        210 119
        142 221
        11 231
        307 279
        137 185
        258 153
        163 49
        86 230
        292 146
        159 80
        204 117
        100 234
        146 190
        44 313
        282 149
        171 61
        111 228
        66 167
        156 169
        126 311
        303 295
        294 267
        117 97
        112 55
        41 292
        236 285
        318 293
        1 218
        239 107
        314 200
        194 112
        48 124
        278 232
        72 256
        275 187
        274 185
        210 192
        29 262
        167 6
        109 18
        297 13
        211 248
        74 276
        159 15
        72 99
        16 99
        166 76
        218 285
        272 30
        271 15
        110 148
        94 121
        126 22
        265 56
        319 274
        37 184
        151 75
        79 206
        133 42
        188 200
        64 28
        87 49
        205 267
        303 318
        46 138
        317 50
        25 222
        8 113
        115 251
        321 75
        313 238
        84 8
        151 99
        159 304
        45 7
        225 269
        208 12
        1 280
        25 309
        283 81
        255 128
        2 221
        20 107
        291 266
        5 225
        315 146
        194 251
        78 272
        148 176
        14 26
        149 249
        265 105
        81 61
        240 186
        242 92
        38 57
        5 147
        85 237
        313 260
        196 275
        39 203
        292 155
        31 82
        60 156
        160 111
        300 263
        180 182
        243 244
        41 213
        278 193
        302 165
        273 54
        242 45
        189 85
        317 293
        103 16
        317 295
        105 190
        73 275
        260 254
        228 49
        22 58
        265 308
        226 42
        4 247
        71 61
        129 192
        67 119
        86 207
        133 137
        180 241
        280 293
        300 269
        115 323
        142 229
        270 234
        99 102
        144 206
        9 259
        81 254
        202 12
        198 322
        201 322
        47 93
        189 312
        317 222
        105 215
        66 169
        202 120
        189 52
        316 320
        64 144
        245 143
        157 210
        203 8
        129 185
        302 45
        201 110
        25 323
        96 71
        110 52
        175 32
        103 231
        38 135
        101 84
        0 43
        280 252
        176 17
        63 224
        62 224
        22 93
        236 50
        281 69
        253 179
        191 46
        246 70
        14 73
        242 77
        43 138
        293 158
        245 247
        179 53
        301 145
        141 28
        285 2
        290 98
        59 109
        27 98
        271 184
        9 236
        66 94
        252 142
        145 182
        106 89
        9 115
        159 44
        18 182
        150 112
        227 167
        62 140
        233 138
        181 46
        74 302
        106 312
        319 58
        296 231
        253 112
        114 213
        23 2
        315 78
        128 230
        191 168
        69 164
        104 241
        248 6
        67 195
        243 301
        225 195
        194 222
        103 98
        248 322
        105 230
        33 32
        171 163
        227 322
        142 309
        314 58
        204 94
        263 306
        232 276
        217 213
        318 75
        183 55
        277 278
        172 126
        241 257
        155 43
        284 195
        68 241
        214 239
        259 102
        141 154
        298 261
        150 29
        130 320
        252 222
        134 111
        100 5
        321 97
        315 255
        174 186
        175 187
        273 182
        141 12
        44 63
        95 127
        250 35
        62 304
        305 63
        40 310
        196 108
        88 59
        224 40
        57 309
        291 238
        173 237
        155 181
        4 30
        198 85
        177 208
        90 305
        0 152
        73 207
        42 125
        246 130
        145 150
        305 310
        297 79
        173 176
        299 140
        221 50
        1 135
        132 57
        199 152
        175 91
        228 80
        3 151
        25 55
        19 82
        165 77
        116 124
        65 271
        157 137
        123 307
        219 53
        88 138
        8 277
        73 272
        218 151
        312 35
        288 135
        202 274
        11 256
        270 153
        101 216
        300 47
        173 232
        20 266
        101 17
        287 40
        98 75
        108 128
        34 60
        57 115
        287 282
        31 233
        89 130
        203 193
        281 74
        101 276
        131 116
        1 102
        87 36
        119 153
        183 307
        227 52
        120 311
        23 259
        125 71
        147 300
        234 67
        36 111
        152 18
        188 311
        21 310
        118 257
        86 186
        232 249
        204 235
        37 127
        118 209
        96 49
        103 235
        144 154
        129 93
        258 141
        219 286
        48 125
        43 109
        268 220
        104 244
        31 245
        24 254
        72 235
        14 33
        65 48
        214 160
        287 76
        65 61
        246 290
        160 15
        196 206
        229 136
        70 156
        247 190
        301 209
        19 46
        20 165
        74 76
        90 299
        54 298
        55 298
        177 314
        95 24
        """

        self.waters = """
        0.4597 0.91941 0.91853
        0.91941 0.4597 0.12847
        0.5403 0.0806 0.12847
        0.95696 0.29303 0.18919
        0.66941 0.95971 0.85586
        0.70833 0.04166 0.62769
        0.70696 0.66393 0.26824
        0.99726 0.37363 0.39842
        0.41667 0.20833 0.33333
        0.0 0.0 0.12014
        0.87363 0.74726 0.74814
        0.66667 0.33333 0.21319
        0.25274 0.12637 0.74814
        0.41667 0.08333 0.83333
        0.87363 0.12637 0.79514
        0.2097 0.7903 0.53795
        0.33333 0.91667 0.16667
        0.29167 0.33333 0.37231
        0.625 0.0 0.96103
        0.66941 0.7097 0.93491
        0.7903 0.58059 0.46205
        0.20696 0.41393 0.4618
        0.95834 0.29167 0.70564
        0.33059 0.0403 0.14414
        0.00274 0.37637 0.52253
        0.33059 0.2903 0.06509
        0.66393 0.95696 0.81081
        0.12637 0.25274 0.20486
        0.04304 0.33607 0.73176
        0.625 0.0 0.03897
        0.66667 0.08333 0.83333
        0.33333 0.66667 0.9085
        0.5403 0.08059 0.76968
        0.7903 0.2097 0.76968
        0.70696 0.04304 0.26824
        0.12637 0.25274 0.25186
        0.87637 0.75274 0.56365
        0.74726 0.87363 0.56365
        0.20696 0.79304 0.10302
        0.0 0.0 0.34942
        0.58607 0.79304 0.4618
        0.54304 0.08607 0.89699
        0.95833 0.66667 0.62769
        0.2903 0.9597 0.93491
        0.25 0.0 0.5
        0.99726 0.62363 0.39842
        0.87637 0.75274 0.92194
        0.20833 0.41667 0.66667
        0.2097 0.7903 0.58861
        0.66667 0.33333 0.57517
        0.58607 0.79304 0.10302
        0.12363 0.24726 0.43635
        0.08333 0.54167 0.30751
        0.125 0.87501 0.0
        0.33333 0.66667 0.01609
        0.375 0.375 0.03897
        0.66941 0.7097 0.85586
        0.12363 0.87637 0.07806
        0.70833 0.04166 0.70564
        0.20834 0.79167 0.97711
        0.54304 0.08607 0.25527
        0.2097 0.4194 0.58861
        0.75 0.0 0.5
        0.37637 0.00274 0.47747
        0.08607 0.54304 0.74473
        0.33333 0.66667 0.57858
        0.12637 0.87363 0.25186
        0.54167 0.45833 0.64378
        0.2903 0.33059 0.93491
        0.41941 0.2097 0.41139
        0.5806 0.7903 0.23032
        0.00274 0.37637 0.60158
        0.95696 0.66393 0.18919
        0.04304 0.33607 0.81081
        0.62637 0.62363 0.39842
        0.33333 0.41667 0.16667
        0.58607 0.79303 0.41481
        0.12363 0.87637 0.43635
        0.0403 0.3306 0.85586
        0.45696 0.91393 0.79538
        0.41393 0.20696 0.5382
        0.12637 0.25274 0.56365
        0.4597 0.5403 0.91853
        0.12637 0.87363 0.56365
        0.54167 0.45833 0.33333
        0.875 0.125 0.31045
        0.04304 0.70697 0.81081
        0.79304 0.58607 0.58519
        0.0 0.625 0.96102
        0.66667 0.33333 0.24525
        0.99726 0.62363 0.47747
        0.5403 0.4597 0.76968
        0.37637 0.00274 0.39842
        0.125 0.25 0.68955
        0.0 0.0 0.24183
        0.79304 0.20696 0.5382
        0.79303 0.20696 0.58519
        0.70697 0.66393 0.18919
        0.33607 0.29303 0.18919
        0.08333 0.66667 0.16667
        0.54167 0.08333 0.64378
        0.45834 0.54167 0.35621
        0.9597 0.66941 0.14414
        0.33607 0.04304 0.18919
        0.41666 0.20833 0.97417
        0.0403 0.7097 0.85586
        0.91393 0.45696 0.25527
        0.62637 0.62363 0.47747
        0.66393 0.70697 0.81081
        0.375 0.0 0.96103
        0.91666 0.45833 0.33333
        0.79304 0.58607 0.5382
        0.625 0.625 0.03897
        0.25 0.125 0.31045
        0.87637 0.12363 0.87129
        0.0 0.0 0.08809
        0.62363 0.99726 0.60158
        0.74726 0.87363 0.20486
        0.0 0.375 0.96102
        0.45833 0.54167 0.66667
        0.04304 0.70697 0.73176
        0.74726 0.87363 0.25186
        0.0806 0.5403 0.23032
        0.66667 0.33334 0.98391
        0.37363 0.99726 0.60158
        0.00274 0.62637 0.60158
        0.91667 0.45834 0.69249
        0.87637 0.12363 0.56365
        0.66667 0.58333 0.83333
        0.0 0.0 0.67982
        0.54304 0.45696 0.25527
        0.58059 0.7903 0.58861
        0.9597 0.66941 0.06509
        0.125 0.875 0.64084
        0.62363 0.62637 0.52253
        0.08607 0.54304 0.10302
        0.9597 0.2903 0.06509
        0.20833 0.79167 0.66667
        0.0403 0.7097 0.93491
        0.91941 0.4597 0.76968
        0.0 0.25 0.5
        0.29304 0.33608 0.73176
        0.5403 0.0806 0.08147
        0.4597 0.5403 0.87153
        0.33333 0.66667 0.75476
        0.75 0.875 0.0
        0.24726 0.12363 0.87129
        0.95833 0.29166 0.62769
        0.08333 0.54166 0.35621
        0.7903 0.2097 0.41139
        0.58333 0.79167 0.02583
        0.08333 0.41667 0.16667
        0.66941 0.9597 0.93491
        0.54166 0.45834 0.69249
        0.45696 0.54304 0.74473
        0.24726 0.12363 0.92194
        0.4597 0.9194 0.23032
        0.45833 0.91667 0.66667
        0.7097 0.66941 0.14414
        0.37363 0.99726 0.52253
        0.00274 0.62637 0.52253
        0.29167 0.95833 0.29436
        0.7903 0.2097 0.46205
        0.41393 0.20696 0.58519
        0.25274 0.12637 0.43635
        0.87363 0.74726 0.43635
        0.33333 0.66667 0.42483
        0.95696 0.66393 0.26824
        0.54304 0.45696 0.89699
        0.2097 0.7903 0.23032
        0.0403 0.33059 0.93491
        0.37363 0.37637 0.60158
        0.08334 0.54167 0.66667
        0.875 0.125 0.35916
        0.7903 0.5806 0.76968
        0.4194 0.2097 0.76968
        0.04167 0.33333 0.37231
        0.87363 0.12637 0.74814
        0.66667 0.33333 0.42142
        0.875 0.75001 0.0
        0.625 0.625 0.96103
        0.0 0.0 0.91191
        0.58334 0.79167 0.97712
        0.41667 0.20834 0.02289
        0.5806 0.7903 0.53795
        0.125 0.875 0.68955
        0.87363 0.74726 0.79514
        0.25274 0.12637 0.79514
        0.70833 0.66667 0.70564
        0.04167 0.33333 0.29436
        0.2903 0.95971 0.85586
        0.79304 0.58607 0.89699
        0.75 0.875 0.68955
        0.29167 0.95833 0.37231
        0.7097 0.66941 0.06509
        0.70833 0.66667 0.62769
        0.45696 0.54304 0.79538
        0.20696 0.41393 0.41481
        0.0 0.0 0.32018
        0.87637 0.12363 0.92194
        0.66392 0.70697 0.73176
        0.79167 0.58333 0.33334
        0.29304 0.95696 0.73176
        0.25 0.125 0.35916
        0.0 0.0 0.21344
        0.66667 0.95833 0.29436
        0.33333 0.66667 0.78681
        0.08607 0.54304 0.79538
        0.0 0.0 0.75817
        0.79167 0.20833 0.97417
        0.58333 0.79167 0.66667
        0.45834 0.54167 0.30751
        0.79167 0.58334 0.97417
        0.79304 0.20696 0.89699
        0.0 0.75 0.5
        0.08059 0.5403 0.87153
        0.33333 0.66667 0.34648
        0.91393 0.45696 0.89699
        0.9597 0.2903 0.14414
        0.20833 0.79167 0.02583
        0.04167 0.70833 0.37231
        0.45696 0.91393 0.10302
        0.5403 0.4597 0.08147
        0.58334 0.91667 0.16667
        0.62637 0.00274 0.47747
        0.75 0.875 0.64084
        0.91667 0.45833 0.64378
        0.04167 0.70833 0.29436
        0.66667 0.33333 0.54677
        0.7097 0.0403 0.06509
        0.91667 0.58333 0.83333
        0.54304 0.08607 0.20462
        0.66667 0.95833 0.37231
        0.0806 0.5403 0.91853
        0.66667 0.33333 0.65352
        0.12637 0.87363 0.20486
        0.75274 0.87637 0.12871
        0.79167 0.20833 0.33333
        0.37637 0.37363 0.47747
        0.75 0.75 0.5
        0.0 0.0 0.78656
        0.375 0.375 0.96103
        0.20697 0.79304 0.41481
        0.125 0.25 0.0
        0.25 0.125 0.0
        0.33333 0.66667 0.8801
        0.4597 0.5403 0.23032
        0.4597 0.91941 0.87153
        0.66667 0.70833 0.29436
        0.62637 0.00274 0.39842
        0.2097 0.4194 0.23032
        0.75274 0.87637 0.07806
        0.66667 0.33334 0.0915
        0.79166 0.58333 0.02289
        0.2097 0.4194 0.53795
        0.41667 0.33333 0.83333
        0.91393 0.45696 0.20462
        0.20833 0.41667 0.97711
        0.33333 0.29167 0.70564
        0.12363 0.87637 0.12871
        0.37363 0.37637 0.52253
        0.0 0.375 0.03897
        0.375 0.0 0.03897
        0.33333 0.29167 0.62769
        0.45696 0.91393 0.74473
        0.87637 0.75274 0.87129
        0.66667 0.33333 0.45347
        0.45833 0.91667 0.30751
        0.875 0.75 0.35916
        0.0 0.0 0.65057
        0.66667 0.33333 0.68276
        0.33333 0.66667 0.54653
        0.91667 0.33333 0.83333
        0.33333 0.66667 0.98685
        0.33333 0.04166 0.70564
        0.29303 0.33607 0.81081
        0.66667 0.70833 0.37231
        0.54167 0.08334 0.33334
        0.45833 0.91667 0.35621
        0.79167 0.20833 0.02289
        0.66667 0.33334 0.1199
        0.37637 0.37363 0.39842
        0.87363 0.12637 0.43635
        0.24726 0.12363 0.56365
        0.62363 0.62637 0.60158
        0.7097 0.0403 0.14414
        0.0 0.625 0.03897
        0.75274 0.87637 0.43635
        0.91941 0.45971 0.08147
        0.33607 0.04304 0.26824
        0.54304 0.45696 0.20462
        0.41941 0.2097 0.46205
        0.41393 0.20696 0.89699
        0.5403 0.4597 0.12847
        0.33333 0.66667 0.31724
        0.20696 0.41393 0.10302
        0.70697 0.04304 0.18919
        0.29303 0.95696 0.81081
        0.20833 0.41667 0.02583
        0.99726 0.37363 0.47747
        0.125 0.25 0.64084
        0.875 0.125 0.0
        0.7903 0.58059 0.41139
        0.12363 0.24726 0.12871
        0.62363 0.99726 0.52253
        0.20696 0.79304 0.4618
        0.33333 0.04167 0.62769
        0.66667 0.33334 0.01315
        0.0 0.0 0.87986
        0.3306 0.0403 0.06509
        0.33333 0.66667 0.45323
        0.95834 0.66667 0.70564
        0.95696 0.29304 0.26824
        0.25 0.25 0.5
        0.66392 0.95696 0.73176
        0.2903 0.3306 0.85586
        0.29167 0.33333 0.29436
        0.45696 0.54304 0.10302
        0.33059 0.2903 0.14414
        0.54166 0.08333 0.69249
        0.33607 0.29304 0.26824
        0.58334 0.66667 0.16667
        0.875 0.75 0.31045
        0.12363 0.24726 0.07806
        """

        self.coord = "relative"

        self.cages = """
        14 1.0000033333333334 0.9999966666666668 0.5279066666666666
        14 1.3333366666666666 0.6666633333333333 -0.8054266666666667
        15 1.3333366666666666 1.6666633333333334 1.4995133333333335
        16 0.33333 0.66667 -0.29439
        12 0.49452333333333337 0.9890466666666667 0.5621966666666667
        16 0.33333 0.66667 0.06436
        15 0.33333 0.66667 -0.16618
        15 0.6666633333333333 1.3333366666666666 0.5004866666666666
        16 1.0000033333333334 0.9999966666666668 0.6023066666666667
        12 -0.16667 0.16666 -0.33333
        12 1.3333366666666666 1.6666633333333334 1.3859233333333334
        12 0.16667 0.33333 0.33333
        12 3.3333333333333333e-06 0.5000066666666666 0.9999966666666668
        16 1.0000033333333334 0.9999966666666668 0.9610566666666667
        12 0.6557133333333333 0.8278566666666667 0.7711366666666667
        12 0.5054766666666667 1.4945233333333334 1.4378033333333333
        12 0.8278566666666667 0.6557133333333333 -0.7711366666666667
        16 0.66667 0.33333 -0.06436
        12 -0.49452333333333337 -0.9890466666666667 -0.5621966666666667
        15 0.9999966666666668 1.0000033333333334 -0.8328466666666667
        12 0.16119 0.32238 -0.10447
        12 0.17214333333333331 0.8278566666666667 0.7711366666666667
        15 1.0000033333333334 0.9999966666666668 0.8328466666666667
        12 0.5000033333333334 0.9999966666666668 0.9999966666666668
        14 0.66667 0.33333 -0.13876
        12 0.33333 0.66667 -0.05259
        12 -0.16119 0.16119 0.10447
        12 0.9999966666666668 1.0000033333333334 -0.7192566666666668
        12 0.49999333333333335 0.49999666666666664 0.9999966666666668
        12 0.16119 -0.16119 -0.10447
        12 0.66667 0.33333 0.05259
        14 0.6666633333333333 1.3333366666666666 0.8054266666666667
        12 0.8278566666666667 0.17214333333333331 -0.7711366666666667
        16 1.3333366666666666 1.6666633333333334 1.6277233333333334
        12 -0.16119 -0.32238 0.10447
        14 0.9999966666666668 2.0000033333333334 1.4720933333333335
        12 0.17214333333333331 0.34428666666666663 0.7711366666666667
        12 0.6666633333333333 1.3333366666666666 0.6140766666666666
        12 -0.32238 -0.16119 -0.10447
        16 0.6666633333333333 1.3333366666666666 0.7310266666666667
        12 1.0000033333333334 0.9999966666666668 0.7192566666666668
        12 -0.6557133333333333 -0.8278566666666667 -0.7711366666666667
        12 0.010953333333333332 0.5054766666666667 0.5621966666666667
        16 0.6666633333333333 1.3333366666666666 0.37227666666666664
        12 0.16666 -0.16667 0.33333
        15 0.66667 0.33333 0.16618
        12 0.9890466666666667 1.4945233333333334 1.4378033333333333
        12 0.33333 0.16667 -0.33333
        16 0.66667 0.33333 0.29439
        12 -0.33333 -0.16666 0.33333
        12 -0.16667 -0.33333 -0.33333
        16 1.3333366666666666 0.6666633333333333 -0.7310266666666667
        12 0.49452333333333337 0.5054766666666667 0.5621966666666667
        16 0.9999966666666668 1.0000033333333334 -0.9610566666666667
        14 0.33333 0.66667 0.13876
        16 0.9999966666666668 2.0000033333333334 1.3976933333333335
        12 0.32238 0.16119 0.10447
        """

        self.bondlen = 3

        self.cell = """
        12.79238210404658 0.0 0.0
        -6.396191052023287 11.078527877021768 0.0
        6.2689533354631446e-15 1.0858145687300545e-14 102.37977741546108
        """

        self.density = 0.6674659339153055

        self.cell = cellvectors(a=12.79238210404658,
                                b=12.792382104046581,
                                c=102.37977741546108,
                                C=119.99999999999999)
