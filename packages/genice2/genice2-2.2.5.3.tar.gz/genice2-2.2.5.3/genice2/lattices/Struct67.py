# coding: utf-8
"""
Data source: Dutour Sikirić, Mathieu, Olaf Delgado-Friedrichs, and Michel Deza. “Space Fullerenes: a Computer Search for New Frank-Kasper Structures” Acta Crystallographica Section A Foundations of Crystallography 66.Pt 5 (2010): 602–615.

Cage composition:
 (12,14,15,16) = (44,8,8,16,)
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
        284 334
        227 67
        51 122
        359 371
        276 294
        219 325
        345 350
        20 291
        396 82
        353 274
        299 327
        7 425
        109 380
        50 283
        277 63
        77 301
        382 279
        369 317
        14 56
        355 365
        351 366
        114 269
        238 241
        383 411
        295 282
        217 168
        225 22
        27 392
        303 324
        231 142
        43 26
        121 176
        276 378
        163 384
        407 178
        130 186
        274 66
        8 69
        115 404
        381 12
        100 80
        158 243
        135 417
        137 236
        357 79
        255 320
        244 366
        171 259
        247 60
        396 92
        44 56
        292 410
        69 97
        136 13
        302 241
        315 83
        316 85
        118 205
        248 423
        45 344
        294 201
        398 327
        84 292
        22 343
        36 299
        403 382
        357 103
        354 103
        388 270
        341 95
        405 287
        415 329
        316 395
        126 313
        228 386
        66 35
        178 11
        221 17
        98 239
        127 192
        210 189
        43 318
        218 375
        414 338
        51 294
        307 251
        52 210
        119 184
        32 416
        193 318
        372 188
        75 74
        8 206
        369 96
        351 330
        107 265
        103 414
        246 117
        232 361
        353 188
        426 265
        95 371
        312 302
        298 55
        144 296
        310 377
        230 3
        118 377
        150 169
        253 376
        115 201
        348 28
        126 263
        370 288
        214 429
        277 416
        155 283
        133 330
        236 411
        240 339
        156 374
        158 288
        191 18
        352 73
        419 323
        227 275
        423 88
        197 401
        428 128
        29 239
        129 45
        304 160
        192 6
        227 346
        364 34
        94 412
        2 184
        198 384
        215 223
        63 179
        14 208
        82 168
        98 182
        199 217
        153 258
        246 242
        235 75
        339 188
        165 80
        109 142
        1 429
        0 166
        345 72
        430 88
        351 377
        261 197
        357 183
        145 291
        210 250
        44 350
        370 271
        337 297
        109 328
        46 90
        237 270
        215 320
        52 24
        274 419
        165 3
        116 86
        125 206
        290 266
        397 23
        335 193
        226 19
        70 325
        4 263
        388 145
        291 6
        131 128
        418 26
        144 210
        118 308
        255 74
        426 247
        180 42
        307 85
        235 422
        335 72
        394 39
        167 273
        120 258
        289 321
        93 99
        367 243
        35 191
        244 30
        302 271
        171 151
        400 280
        198 39
        110 385
        54 317
        201 424
        68 428
        380 160
        257 129
        140 266
        72 376
        176 314
        121 150
        399 92
        90 229
        392 141
        58 421
        235 297
        202 146
        348 313
        213 138
        135 204
        137 205
        311 179
        36 188
        226 61
        2 72
        14 399
        253 393
        27 18
        121 35
        41 293
        107 13
        101 80
        345 119
        234 32
        58 26
        2 197
        326 347
        167 70
        353 180
        64 89
        52 59
        332 427
        209 206
        218 101
        104 91
        185 402
        262 378
        130 100
        349 266
        49 39
        430 427
        222 175
        389 205
        65 349
        200 101
        348 241
        170 255
        111 329
        3 42
        123 9
        29 158
        155 6
        213 408
        20 195
        134 319
        102 43
        372 418
        319 265
        430 51
        108 59
        83 133
        251 322
        174 33
        396 321
        358 392
        208 166
        248 15
        89 321
        78 309
        150 374
        237 385
        20 303
        1 334
        96 331
        304 28
        145 127
        346 148
        270 16
        239 367
        199 224
        341 85
        248 428
        108 21
        287 23
        228 223
        92 25
        383 162
        267 196
        116 216
        263 71
        417 114
        274 18
        223 239
        407 202
        161 365
        333 265
        73 242
        2 117
        426 97
        38 146
        277 110
        53 196
        134 125
        13 164
        409 168
        300 400
        346 244
        91 259
        215 252
        337 111
        385 155
        356 121
        139 375
        175 414
        110 16
        158 386
        313 182
        298 102
        222 172
        1 77
        293 196
        262 424
        136 97
        419 272
        256 117
        38 421
        14 286
        342 212
        359 395
        237 291
        420 250
        238 59
        202 405
        132 422
        398 275
        123 24
        390 184
        192 114
        294 382
        189 270
        48 76
        36 176
        212 362
        115 214
        6 324
        257 390
        76 331
        391 211
        385 282
        408 293
        368 401
        249 247
        418 93
        347 122
        220 100
        352 431
        174 317
        78 160
        359 431
        322 362
        405 99
        5 412
        342 320
        253 193
        361 394
        64 386
        137 156
        54 431
        332 153
        263 420
        21 311
        233 290
        119 301
        336 71
        407 284
        234 379
        98 206
        162 381
        221 413
        262 428
        368 246
        249 32
        351 140
        356 141
        215 309
        289 62
        19 373
        73 371
        124 197
        225 369
        406 79
        157 98
        238 83
        198 106
        151 79
        231 105
        233 172
        412 214
        218 410
        220 392
        0 399
        273 394
        115 281
        172 46
        153 319
        49 398
        149 395
        339 314
        285 12
        25 223
        259 360
        260 360
        315 302
        316 303
        305 350
        126 271
        208 94
        308 189
        421 318
        362 255
        31 173
        177 84
        147 352
        404 365
        395 195
        124 254
        408 112
        173 75
        59 41
        333 60
        66 278
        68 279
        79 140
        213 127
        306 41
        307 45
        378 279
        341 57
        323 411
        184 413
        47 164
        207 74
        166 119
        167 32
        231 194
        148 384
        65 189
        132 170
        69 181
        389 96
        200 139
        315 190
        358 80
        50 282
        159 319
        280 87
        104 260
        131 90
        108 245
        67 70
        5 7
        405 26
        383 266
        229 86
        364 67
        429 409
        102 416
        423 224
        391 422
        4 182
        308 112
        64 280
        276 425
        219 418
        47 216
        111 161
        84 207
        373 15
        214 186
        49 219
        160 360
        165 334
        174 22
        64 17
        335 401
        358 42
        179 267
        226 10
        147 138
        328 320
        154 200
        313 367
        250 190
        303 242
        393 287
        420 311
        234 9
        290 406
        391 252
        253 417
        193 283
        211 309
        99 178
        402 338
        89 25
        102 273
        111 169
        38 301
        187 60
        363 381
        65 33
        311 41
        231 84
        143 146
        63 24
        326 120
        209 159
        306 250
        230 305
        431 96
        145 54
        369 191
        31 104
        67 285
        149 150
        151 152
        332 300
        355 329
        77 286
        130 404
        236 349
        152 91
        357 90
        49 11
        136 120
        132 207
        285 47
        254 371
        372 81
        58 305
        388 408
        398 264
        152 172
        368 283
        292 365
        310 112
        262 224
        149 48
        430 425
        62 82
        156 317
        318 55
        110 135
        340 243
        348 78
        143 376
        288 157
        113 7
        52 16
        341 242
        131 268
        53 114
        336 8
        379 187
        116 347
        245 241
        332 87
        185 61
        275 325
        233 330
        124 324
        373 88
        209 62
        1 7
        211 340
        183 152
        300 82
        333 181
        295 267
        397 204
        109 91
        284 38
        331 141
        281 101
        31 142
        139 48
        363 414
        373 122
        37 15
        345 146
        278 323
        44 335
        202 305
        77 203
        378 410
        342 340
        268 104
        129 261
        142 74
        28 190
        343 366
        419 106
        81 284
        257 401
        354 12
        81 240
        30 140
        135 196
        375 75
        34 167
        306 83
        94 113
        228 400
        327 387
        393 204
        51 217
        213 53
        23 394
        4 123
        199 429
        388 33
        338 15
        264 272
        177 173
        298 295
        360 211
        425 224
        355 207
        379 181
        396 286
        415 85
        400 92
        21 60
        298 23
        301 56
        187 232
        343 411
        300 159
        99 39
        336 333
        35 156
        310 33
        34 361
        94 409
        125 289
        337 76
        12 40
        212 17
        113 203
        50 269
        337 375
        387 18
        307 170
        62 120
        252 344
        370 71
        95 322
        225 387
        161 218
        191 141
        292 424
        272 343
        168 427
        133 296
        361 384
        176 220
        93 106
        30 40
        143 55
        180 178
        36 66
        37 68
        363 185
        10 347
        137 278
        87 203
        234 63
        29 89
        308 138
        126 190
        65 296
        352 127
        144 28
        30 103
        304 171
        256 192
        372 11
        130 314
        310 133
        95 297
        46 380
        179 187
        8 4
        353 93
        268 183
        299 27
        107 258
        105 128
        19 107
        199 201
        21 71
        316 254
        248 116
        268 68
        228 157
        57 221
        88 258
        359 76
        315 171
        282 53
        381 222
        281 276
        364 148
        246 390
        10 136
        216 338
        415 297
        113 427
        423 326
        209 97
        162 366
        200 404
        277 295
        225 205
        323 275
        186 334
        54 195
        261 413
        424 105
        13 181
        387 272
        208 350
        148 185
        9 247
        285 61
        118 349
        220 169
        356 48
        143 287
        78 328
        368 324
        290 296
        177 422
        354 229
        256 73
        252 170
        230 240
        402 164
        293 16
        43 393
        251 254
        289 153
        5 281
        403 86
        108 123
        37 175
        125 29
        134 288
        235 362
        299 11
        403 122
        166 203
        356 154
        336 134
        358 154
        312 340
        198 264
        391 212
        256 124
        238 144
        383 40
        304 406
        204 416
        321 87
        194 260
        222 229
        42 339
        331 169
        412 230
        364 164
        269 117
        174 236
        221 322
        377 22
        31 279
        233 162
        397 232
        312 259
        5 165
        163 70
        154 314
        149 329
        389 374
        245 182
        376 269
        147 389
        226 426
        363 244
        227 40
        151 330
        129 399
        245 370
        344 17
        342 386
        355 139
        163 61
        261 251
        132 415
        326 217
        86 128
        346 264
        180 27
        69 9
        37 403
        81 58
        243 271
        46 406
        19 402
        306 112
        410 173
        0 280
        278 327
        186 240
        20 147
        309 367
        312 328
        177 260
        0 413
        219 273
        382 105
        44 421
        237 138
        175 183
        420 24
        155 417
        106 325
        195 374
        131 194
        57 390
        34 379
        10 47
        407 3
        257 56
        354 216
        194 380
        249 163
        25 344
        50 55
        157 159
        249 232
        397 267
        161 100
        286 409
        57 45
        """

        self.waters = """
        0.125 0.2708 0.06008
        0.5 0.2923 0.29678
        0.19042 0.42266 0.02212
        0.19726 0.41667 0.35098
        0.69042 0.92266 0.02212
        0.19726 0.30414 0.3617
        0.875 0.54815 0.91348
        0.32226 0.25923 0.31946
        0.625 0.95185 0.08653
        0.82226 0.86024 0.12033
        0.82226 0.966 0.30874
        0.5 0.5597 0.37567
        0.81542 0.86617 0.46216
        0.5 0.92955 0.25
        0.80274 0.30414 0.1383
        0.30959 0.01705 0.41375
        0.875 0.72921 0.93992
        0.375 0.22921 0.93992
        0.19042 0.57735 0.52212
        0.17774 0.966 0.30874
        0.67774 0.534 0.80874
        0.18459 0.86617 0.03784
        0.19726 0.69587 0.6383
        0.31542 0.6435 0.18481
        0.69042 0.8098 0.00027
        0.69042 0.1902 0.99973
        0.875 0.55741 0.25
        0.31542 0.52924 0.48001
        0.69042 0.91331 0.8106
        0.5 0.09444 0.01972
        0.5 0.83704 0.53544
        0.17774 0.13977 0.62033
        0.82226 0.75923 0.18054
        0.0 0.70685 0.75
        0.5 0.79316 0.25
        0.875 0.54815 0.58653
        0.68459 0.52924 0.48001
        0.18459 0.02924 0.48001
        0.5 0.43087 0.20935
        0.31542 0.6435 0.31519
        0.69042 0.8098 0.49973
        0.18459 0.78901 0.94019
        0.125 0.45185 0.41348
        0.80959 0.58669 0.1894
        0.80274 0.41667 0.14903
        0.68459 0.28901 0.94019
        0.81542 0.96959 0.64876
        0.69726 0.91667 0.35098
        0.0 0.39744 0.64689
        0.5 0.6286 0.3577
        0.5 0.55848 0.03998
        0.0 0.1286 0.3577
        0.81542 0.78901 0.94019
        0.31542 0.63383 0.96216
        0.0 0.57045 0.75
        0.5 0.5597 0.12433
        0.67774 0.36024 0.12033
        0.5 0.32828 0.93592
        0.80274 0.4781 0.25
        0.0 0.82828 0.93592
        0.17774 0.86024 0.12033
        0.0 0.86102 0.33743
        0.69042 0.08669 0.1894
        0.625 0.7708 0.06008
        0.30959 0.1902 0.99973
        0.80274 0.75254 0.75
        0.80959 0.57735 0.52212
        0.69726 0.80414 0.3617
        0.30959 0.07735 0.52212
        0.69726 0.91667 0.14903
        0.82226 0.75923 0.31946
        0.30959 0.92266 0.02212
        0.125 0.45185 0.08653
        0.31542 0.46959 0.85125
        0.0 0.20771 0.70322
        0.17774 0.24077 0.68054
        0.19042 0.41331 0.6894
        0.5 0.2923 0.20322
        0.82226 0.034 0.80874
        0.5 0.89744 0.64689
        0.31542 0.36617 0.46216
        0.67774 0.466 0.30874
        0.81542 0.1435 0.18481
        0.18459 0.85651 0.81519
        0.69726 0.19587 0.6383
        0.68459 0.35651 0.81519
        0.81542 0.02924 0.48001
        0.30959 0.19865 0.13803
        0.30959 0.08669 0.3106
        0.5 0.16296 0.03544
        0.69042 0.98295 0.58626
        0.17774 0.034 0.69127
        0.81542 0.211 0.05981
        0.0 0.60257 0.35311
        0.0 0.29316 0.25
        0.31542 0.35651 0.81519
        0.32226 0.534 0.69127
        0.82226 0.966 0.19127
        0.81542 0.02924 0.01999
        0.19042 0.58669 0.3106
        0.5 0.37289 0.50241
        0.19042 0.3098 0.49973
        0.68459 0.6435 0.18481
        0.5 0.90556 0.51972
        0.30274 0.08333 0.64903
        0.81542 0.13383 0.53784
        0.0 0.67113 0.3818
        0.30274 0.9781 0.25
        0.0 0.87289 0.99759
        0.0 0.06913 0.70935
        0.80959 0.6902 0.99973
        0.5 0.3714 0.6423
        0.32226 0.74077 0.81946
        0.19726 0.24747 0.25
        0.19042 0.57735 0.97788
        0.875 0.2708 0.43992
        0.69042 0.01705 0.41375
        0.31542 0.47076 0.98001
        0.5 0.70771 0.70322
        0.32226 0.36024 0.12033
        0.625 0.05741 0.25
        0.80959 0.48295 0.58626
        0.0 0.0597 0.37567
        0.81542 0.86617 0.03784
        0.0 0.44157 0.91561
        0.5 0.05843 0.08439
        0.5 0.94157 0.91561
        0.19726 0.58333 0.85098
        0.69042 0.07735 0.52212
        0.80959 0.3098 0.00027
        0.68459 0.36617 0.46216
        0.625 0.04815 0.58653
        0.69726 0.25254 0.75
        0.125 0.82899 0.75
        0.30959 0.01705 0.08626
        0.0 0.66296 0.03544
        0.69726 0.9781 0.25
        0.67774 0.63977 0.62033
        0.5 0.63898 0.83743
        0.0 0.32887 0.6182
        0.5 0.82887 0.6182
        0.19042 0.48295 0.58626
        0.0 0.13898 0.66257
        0.31542 0.53042 0.14876
        0.81542 0.85651 0.81519
        0.0 0.60636 0.81033
        0.32226 0.466 0.19127
        0.5 0.56913 0.79065
        0.30274 0.80414 0.3617
        0.80959 0.41331 0.6894
        0.68459 0.46959 0.64876
        0.30959 0.91331 0.6894
        0.18459 0.96959 0.64876
        0.30959 0.08669 0.1894
        0.0 0.40556 0.51972
        0.80959 0.57735 0.97788
        0.80274 0.58333 0.64903
        0.0 0.05848 0.03998
        0.30959 0.07735 0.97788
        0.0 0.0597 0.12433
        0.69726 0.02191 0.75
        0.5 0.32828 0.56408
        0.0 0.82828 0.56408
        0.0 0.7923 0.29678
        0.5 0.89364 0.31033
        0.32226 0.36024 0.37967
        0.19726 0.30414 0.1383
        0.69726 0.74747 0.25
        0.875 0.17101 0.25
        0.5 0.4403 0.62433
        0.82226 0.24077 0.81946
        0.375 0.9426 0.75
        0.0 0.9403 0.62433
        0.30274 0.19587 0.6383
        0.0 0.67456 0.68508
        0.18459 0.97076 0.51999
        0.68459 0.47076 0.51999
        0.5 0.17456 0.68508
        0.31542 0.53042 0.35125
        0.375 0.7708 0.06008
        0.19042 0.51705 0.41375
        0.5 0.89364 0.18967
        0.81542 0.97076 0.98001
        0.30959 0.98295 0.58626
        0.31542 0.36617 0.03784
        0.17774 0.86024 0.37967
        0.67774 0.36024 0.37967
        0.30274 0.80414 0.1383
        0.80959 0.51705 0.41375
        0.67774 0.74077 0.81946
        0.5 0.89744 0.85311
        0.125 0.54815 0.58653
        0.125 0.54815 0.91348
        0.80959 0.51705 0.08626
        0.69726 0.08333 0.64903
        0.80274 0.52191 0.75
        0.19042 0.6902 0.99973
        0.0 0.40556 0.98028
        0.19042 0.69865 0.36197
        0.69042 0.19865 0.36197
        0.0 0.33704 0.53544
        0.81542 0.211 0.44019
        0.19726 0.4781 0.25
        0.32226 0.25923 0.18054
        0.0 0.67113 0.1182
        0.5 0.63898 0.66257
        0.69042 0.01705 0.08626
        0.82226 0.24077 0.68054
        0.0 0.32544 0.18508
        0.81542 0.03042 0.14876
        0.69042 0.80136 0.86197
        0.5 0.10636 0.81033
        0.30274 0.19587 0.8617
        0.32226 0.63977 0.87967
        0.80274 0.30414 0.3617
        0.82226 0.13977 0.87967
        0.625 0.95185 0.41348
        0.81542 0.1435 0.31519
        0.31542 0.28901 0.55981
        0.68459 0.6435 0.31519
        0.5 0.44152 0.53998
        0.31542 0.28901 0.94019
        0.0 0.94152 0.53998
        0.81542 0.13383 0.96216
        0.5 0.17113 0.3818
        0.32226 0.63977 0.62033
        0.0 0.93087 0.29065
        0.625 0.7708 0.43992
        0.0 0.12711 0.00241
        0.81542 0.97076 0.51999
        0.0 0.39364 0.31033
        0.82226 0.13977 0.62033
        0.17774 0.75923 0.18054
        0.0 0.8714 0.6423
        0.69726 0.80414 0.1383
        0.30274 0.25254 0.75
        0.80274 0.69587 0.6383
        0.67774 0.63977 0.87967
        0.0 0.8714 0.8577
        0.69042 0.07735 0.97788
        0.80274 0.41667 0.35098
        0.0 0.9403 0.87567
        0.5 0.4403 0.87567
        0.375 0.04815 0.91348
        0.30959 0.8098 0.49973
        0.0 0.94152 0.96002
        0.5 0.44152 0.96002
        0.0 0.86102 0.16257
        0.5 0.05843 0.41561
        0.0 0.7923 0.20322
        0.5 0.82887 0.8818
        0.0 0.32887 0.8818
        0.69726 0.19587 0.8617
        0.0 0.55843 0.08439
        0.0 0.39744 0.85311
        0.0 0.20771 0.79678
        0.19042 0.48295 0.91375
        0.68459 0.36617 0.03784
        0.375 0.05741 0.25
        0.30274 0.02191 0.75
        0.5 0.10636 0.68967
        0.0 0.33704 0.96456
        0.5 0.16296 0.46456
        0.5 0.90556 0.98028
        0.31542 0.711 0.44019
        0.17774 0.966 0.19127
        0.69042 0.80136 0.63803
        0.31542 0.711 0.05981
        0.375 0.04815 0.58653
        0.31542 0.52924 0.01999
        0.80274 0.69587 0.8617
        0.30959 0.98295 0.91375
        0.19042 0.6902 0.50027
        0.625 0.67101 0.25
        0.0 0.59444 0.48028
        0.68459 0.711 0.44019
        0.18459 0.211 0.44019
        0.68459 0.711 0.05981
        0.68459 0.63383 0.53784
        0.18459 0.13383 0.53784
        0.18459 0.211 0.05981
        0.125 0.2708 0.43992
        0.5 0.62711 0.00241
        0.68459 0.52924 0.01999
        0.5 0.43087 0.29065
        0.82226 0.86024 0.37967
        0.67774 0.25923 0.18054
        0.19042 0.58669 0.1894
        0.18459 0.02924 0.01999
        0.5 0.10257 0.14689
        0.81542 0.85651 0.68481
        0.80274 0.58333 0.85098
        0.625 0.22921 0.56008
        0.125 0.72921 0.93992
        0.0 0.17172 0.43592
        0.5 0.67172 0.06408
        0.875 0.82899 0.75
        0.375 0.32899 0.75
        0.5 0.6286 0.1423
        0.5 0.55848 0.46002
        0.0 0.1286 0.1423
        0.5 0.36102 0.16257
        0.18459 0.96959 0.85125
        0.68459 0.46959 0.85125
        0.625 0.9426 0.75
        0.0 0.42955 0.25
        0.30959 0.80136 0.86197
        0.80959 0.30136 0.86197
        0.5 0.70771 0.79678
        0.69726 0.08333 0.85098
        0.19726 0.75254 0.75
        0.30959 0.8098 0.00027
        0.17774 0.034 0.80874
        0.69042 0.98295 0.91375
        0.80959 0.42266 0.47788
        0.30959 0.91331 0.8106
        0.80959 0.41331 0.8106
        0.0 0.60636 0.68967
        0.68459 0.53042 0.14876
        0.18459 0.03042 0.14876
        0.0 0.13898 0.83743
        0.5 0.17113 0.1182
        0.19042 0.30136 0.86197
        0.80959 0.6902 0.50027
        0.80959 0.48295 0.91375
        0.80959 0.69865 0.36197
        0.69042 0.08669 0.3106
        0.5 0.62711 0.49759
        0.0 0.06913 0.79065
        0.68459 0.35651 0.68481
        0.18459 0.85651 0.68481
        0.31542 0.46959 0.64876
        0.18459 0.1435 0.18481
        0.30274 0.91667 0.14903
        0.5 0.36102 0.33743
        0.875 0.45185 0.08653
        0.375 0.95185 0.08653
        0.31542 0.35651 0.68481
        0.375 0.95185 0.41348
        0.875 0.45185 0.41348
        0.30274 0.08333 0.85098
        0.5 0.3714 0.8577
        0.17774 0.13977 0.87967
        0.125 0.72921 0.56008
        0.625 0.22921 0.93992
        0.19726 0.41667 0.14903
        0.375 0.7708 0.43992
        0.81542 0.03042 0.35125
        0.81542 0.96959 0.85125
        0.67774 0.74077 0.68054
        0.0 0.39364 0.18967
        0.30959 0.80136 0.63803
        0.32226 0.534 0.80874
        0.0 0.55843 0.41561
        0.69042 0.92266 0.47788
        0.80959 0.30136 0.63803
        0.0 0.44157 0.58439
        0.5 0.94157 0.58439
        0.19042 0.42266 0.47788
        0.125 0.4426 0.75
        0.5 0.07045 0.75
        0.30274 0.74747 0.25
        0.17774 0.24077 0.81946
        0.18459 0.86617 0.46216
        0.5 0.82544 0.31492
        0.68459 0.28901 0.55981
        0.18459 0.78901 0.55981
        0.625 0.04815 0.91348
        0.68459 0.47076 0.98001
        0.19726 0.58333 0.64903
        0.18459 0.97076 0.98001
        0.19042 0.41331 0.8106
        0.68459 0.53042 0.35125
        0.18459 0.03042 0.35125
        0.67774 0.534 0.69127
        0.19042 0.30136 0.63803
        0.19042 0.51705 0.08626
        0.32226 0.74077 0.68054
        0.30959 0.1902 0.50027
        0.5 0.82544 0.18508
        0.82226 0.034 0.69127
        0.0 0.87289 0.50241
        0.0 0.12711 0.49759
        0.81542 0.78901 0.55981
        0.17774 0.75923 0.31946
        0.68459 0.63383 0.96216
        0.18459 0.13383 0.96216
        0.31542 0.63383 0.53784
        0.0 0.67456 0.81492
        0.5 0.56913 0.70935
        0.5 0.37289 0.99759
        0.5 0.17456 0.81492
        0.31542 0.47076 0.51999
        0.0 0.60257 0.14689
        0.375 0.67101 0.25
        0.875 0.4426 0.75
        0.69042 0.19865 0.13803
        0.19042 0.69865 0.13803
        0.5 0.67172 0.43592
        0.875 0.2708 0.06008
        0.0 0.17172 0.06408
        0.80959 0.42266 0.02212
        0.30274 0.91667 0.35098
        0.0 0.05848 0.46002
        0.80959 0.3098 0.49973
        0.125 0.55741 0.25
        0.69042 0.91331 0.6894
        0.32226 0.466 0.30874
        0.19726 0.69587 0.8617
        0.80274 0.24747 0.25
        0.375 0.22921 0.56008
        0.875 0.72921 0.56008
        0.0 0.32544 0.31492
        0.19042 0.3098 0.00027
        0.30959 0.92266 0.47788
        0.625 0.32899 0.75
        0.80959 0.69865 0.13803
        0.0 0.59444 0.01972
        0.80959 0.58669 0.3106
        0.0 0.66296 0.46456
        0.5 0.83704 0.96456
        0.67774 0.466 0.19127
        0.5 0.20685 0.75
        0.5 0.10257 0.35311
        0.69042 0.1902 0.50027
        0.30959 0.19865 0.36197
        0.0 0.93087 0.20935
        0.125 0.17101 0.25
        0.5 0.09444 0.48028
        0.67774 0.25923 0.31946
        0.18459 0.1435 0.31519
        0.19726 0.52191 0.75
        """

        self.coord = "relative"

        self.cages = """
        12 0.73834 0.61696 0.07996
        12 0.0 0.5 0.0
        14 0.28904 -0.35929 -0.25
        12 0.73834 0.61696 -0.57996
        12 0.0 0.35616 0.08104
        15 0.0 -0.04858 -0.58741
        12 0.5 0.72702 0.34072
        12 -0.23834 0.11696 0.42004
        16 0.0 0.05347 0.25
        12 0.73834 0.38304 -0.42004
        14 -0.28904 0.35929 0.25
        12 0.5 0.0 0.5
        14 -0.28904 -0.35929 0.75
        12 -0.23834 0.11696 0.07996
        12 0.5 0.85616 0.41896
        12 0.23834 -0.11696 -0.07996
        16 0.0 0.22593 0.56288
        12 0.0 -0.22702 0.65928
        15 0.5 0.45142 1.08741
        12 0.0 -0.35616 -0.08104
        16 0.0 0.77407 0.43712
        12 0.26166 0.38304 -0.07996
        16 1.0 0.67653 0.25
        12 0.5 0.99981 0.17765
        14 0.78904 0.85929 0.25
        12 0.0 0.49981 0.32235
        16 -0.5 -0.27407 0.56288
        12 0.26166 0.38304 0.57996
        16 0.0 0.32347 0.75
        12 0.5 0.99981 0.32235
        16 0.5 0.27407 0.06288
        12 0.26166 0.61696 0.42004
        12 0.5 0.00019 -0.17765
        15 0.0 0.04858 -0.08741
        14 0.21096 0.85929 0.25
        12 0.0 -0.5 0.5
        15 0.5 0.54858 0.58741
        16 0.0 -0.05347 0.75
        12 0.5 0.27298 -0.15928
        12 0.5 0.14384 0.58104
        15 0.5 0.54858 -0.08741
        12 0.0 -0.49981 0.67765
        12 0.0 0.35616 0.41896
        12 0.0 0.49981 0.17765
        16 -0.5 -0.17653 0.75
        16 1.0 0.77407 0.06288
        16 -0.5 -0.27407 -0.06288
        12 0.5 0.85616 0.08104
        15 0.5 0.45142 -0.58741
        12 0.0 0.22702 0.34072
        16 0.5 0.55347 0.25
        14 0.21096 0.14071 0.75
        12 0.5 0.00019 0.67765
        16 0.5 0.44653 0.75
        12 0.5 0.27298 0.65928
        12 0.0 -0.22702 -0.15928
        15 0.0 -0.04858 1.08741
        12 0.5 0.14384 -0.08104
        12 -0.23834 -0.11696 -0.07996
        16 0.5 0.17653 0.25
        12 0.23834 0.11696 0.07996
        12 0.5 1.0 0.0
        14 0.78904 0.14071 -0.25
        12 -0.23834 -0.11696 0.57996
        12 0.23834 0.11696 -0.57996
        14 0.28904 0.35929 0.25
        12 0.5 0.72702 0.15928
        12 0.0 0.22702 0.15928
        12 0.23834 -0.11696 -0.42004
        12 0.0 -0.49981 -0.17765
        16 0.0 0.22593 -0.06288
        12 0.73834 0.38304 -0.07996
        12 0.0 -0.35616 0.58104
        16 -0.5 0.27407 0.43712
        15 0.0 0.04858 0.58741
        12 0.26166 0.61696 0.07996
        """

        self.bondlen = 3

        self.cell = """
        13.994099434794087 43.99715431818161 39.23553200872876
        """

        self.density = 0.5345230179314624

        self.cell = cellvectors(a=13.994099434794087,
                                b=43.99715431818161,
                                c=39.23553200872876)
