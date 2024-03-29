# coding: utf-8
"""
Data source: Dutour Sikirić, Mathieu, Olaf Delgado-Friedrichs, and Michel Deza. “Space Fullerenes: a Computer Search for New Frank-Kasper Structures” Acta Crystallographica Section A Foundations of Crystallography 66.Pt 5 (2010): 602–615.

Cage composition:
 (12,14,15,16) = (40,16,16,8,)
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
        82 209
        424 30
        288 5
        178 356
        12 363
        358 179
        102 189
        282 405
        413 374
        265 106
        452 192
        143 363
        79 236
        313 408
        405 415
        132 268
        320 106
        145 70
        397 186
        345 63
        243 1
        180 24
        14 127
        195 293
        133 71
        72 97
        16 115
        17 117
        271 252
        14 402
        349 263
        321 302
        93 450
        365 416
        333 440
        281 362
        454 187
        29 331
        241 56
        226 362
        369 398
        54 273
        207 218
        34 42
        208 190
        61 436
        348 75
        177 188
        410 94
        261 268
        104 28
        218 444
        1 101
        446 86
        244 354
        283 373
        310 127
        378 163
        194 442
        188 378
        4 250
        224 336
        245 39
        200 289
        384 242
        148 411
        72 170
        42 216
        238 175
        391 327
        18 367
        228 408
        187 382
        66 270
        445 121
        165 214
        256 95
        161 57
        164 450
        225 157
        165 414
        168 388
        305 127
        295 112
        33 141
        192 335
        65 172
        394 217
        373 215
        338 337
        419 257
        78 30
        274 199
        81 236
        304 16
        230 340
        429 173
        94 153
        123 302
        124 301
        24 274
        312 293
        441 220
        23 382
        132 296
        185 46
        233 105
        125 221
        394 402
        33 118
        389 317
        161 338
        335 51
        308 66
        266 220
        211 304
        9 395
        198 139
        282 398
        246 353
        394 257
        168 113
        256 192
        105 114
        432 75
        217 329
        267 261
        235 245
        431 73
        81 393
        346 76
        321 446
        455 66
        352 279
        341 421
        0 264
        57 435
        355 142
        125 173
        442 210
        15 263
        176 354
        397 71
        156 184
        162 302
        237 440
        424 451
        308 107
        49 423
        77 400
        182 444
        377 270
        225 202
        151 111
        218 324
        387 136
        32 326
        66 294
        68 427
        174 53
        359 47
        205 16
        300 221
        434 162
        265 292
        8 258
        44 358
        307 181
        158 311
        393 453
        193 132
        252 106
        43 26
        317 291
        322 342
        369 433
        384 108
        227 281
        89 117
        243 32
        33 17
        111 90
        418 35
        40 409
        75 378
        76 347
        308 116
        91 98
        432 337
        380 110
        230 190
        155 120
        418 220
        32 236
        286 152
        350 215
        417 126
        182 116
        64 288
        184 173
        58 114
        427 341
        388 263
        244 372
        136 25
        31 217
        2 370
        376 5
        344 433
        251 112
        224 320
        130 439
        359 312
        10 299
        80 172
        272 332
        369 51
        133 176
        152 284
        35 166
        350 173
        344 6
        281 139
        433 149
        322 309
        334 45
        59 20
        9 423
        271 79
        72 450
        142 169
        359 119
        166 89
        323 40
        62 403
        68 300
        69 301
        325 336
        16 333
        26 191
        241 280
        245 226
        228 244
        251 37
        214 398
        371 297
        164 453
        278 25
        227 381
        225 163
        189 409
        307 305
        15 91
        391 38
        100 339
        360 420
        203 418
        253 381
        264 21
        354 296
        122 55
        154 300
        155 301
        412 396
        5 443
        116 74
        101 428
        427 102
        233 10
        254 228
        404 382
        119 392
        227 159
        56 298
        365 130
        146 103
        376 222
        139 60
        280 328
        95 305
        42 285
        59 343
        224 174
        230 252
        266 409
        82 396
        410 193
        415 250
        232 430
        336 119
        435 48
        425 356
        204 342
        370 320
        280 155
        163 337
        334 196
        290 137
        331 19
        360 62
        241 69
        285 451
        380 151
        161 171
        265 425
        266 426
        141 436
        321 219
        42 54
        216 116
        393 126
        219 291
        210 75
        51 390
        113 132
        232 222
        14 408
        397 144
        251 24
        226 322
        25 229
        114 311
        9 26
        446 341
        243 110
        183 85
        413 262
        224 90
        248 293
        59 172
        261 439
        148 253
        128 353
        352 130
        152 381
        179 409
        407 90
        247 259
        12 19
        58 136
        237 417
        350 262
        434 421
        325 312
        214 418
        165 323
        87 345
        367 407
        0 172
        368 140
        446 225
        234 343
        84 372
        110 356
        286 309
        154 403
        240 77
        197 184
        189 389
        324 52
        267 438
        396 150
        144 104
        126 79
        383 162
        349 346
        286 455
        234 352
        2 208
        206 335
        284 159
        407 404
        56 97
        387 368
        329 306
        99 206
        7 158
        41 354
        36 97
        389 250
        259 288
        195 351
        188 291
        180 272
        201 58
        364 175
        77 189
        8 52
        375 143
        378 88
        98 153
        396 298
        149 426
        212 108
        175 35
        447 157
        235 135
        411 444
        388 268
        296 251
        110 83
        370 119
        304 55
        109 180
        384 112
        196 130
        2 340
        223 293
        316 221
        98 439
        60 64
        49 298
        134 88
        100 174
        155 352
        33 166
        344 335
        186 448
        266 275
        267 274
        350 147
        401 19
        271 249
        318 246
        171 421
        391 297
        95 383
        5 412
        233 186
        4 402
        318 88
        447 11
        449 12
        395 292
        200 449
        223 430
        148 270
        148 269
        211 54
        123 452
        85 74
        147 13
        233 138
        195 129
        240 147
        74 273
        307 402
        76 176
        424 290
        406 401
        364 6
        255 357
        316 413
        313 177
        403 61
        428 97
        24 146
        247 135
        178 292
        167 248
        330 430
        162 131
        37 121
        190 145
        193 158
        349 80
        227 429
        313 394
        15 399
        405 134
        212 65
        133 315
        449 450
        34 44
        287 277
        213 70
        269 436
        309 430
        203 96
        370 67
        128 299
        279 98
        144 368
        276 303
        99 6
        255 264
        107 314
        84 408
        452 383
        265 103
        69 191
        50 202
        371 167
        375 129
        183 323
        185 51
        327 30
        385 437
        53 260
        443 453
        154 345
        158 438
        22 104
        88 202
        121 357
        413 54
        290 107
        242 45
        371 386
        362 204
        319 229
        425 45
        99 95
        237 78
        122 294
        346 71
        333 30
        48 305
        256 390
        273 55
        342 431
        424 169
        0 332
        395 332
        3 102
        299 432
        386 247
        434 258
        254 379
        207 35
        28 338
        101 249
        411 420
        165 358
        124 21
        20 357
        241 43
        128 210
        455 137
        385 276
        219 163
        421 157
        245 211
        23 199
        207 141
        7 306
        92 414
        363 289
        58 7
        375 213
        23 146
        386 309
        1 178
        3 179
        319 447
        99 434
        73 29
        197 281
        14 46
        194 347
        3 13
        435 387
        81 36
        160 56
        431 443
        440 73
        423 236
        18 339
        103 187
        401 326
        315 348
        328 279
        254 7
        125 13
        27 48
        355 284
        28 140
        391 213
        318 348
        364 203
        366 454
        316 39
        177 246
        135 64
        4 96
        12 126
        204 115
        399 279
        82 72
        262 40
        238 192
        138 128
        44 183
        260 153
        11 246
        369 415
        375 205
        361 455
        244 113
        232 312
        70 331
        44 303
        124 209
        113 306
        440 60
        228 201
        194 138
        395 83
        217 181
        283 400
        231 131
        377 385
        222 170
        195 47
        322 135
        417 145
        96 390
        454 106
        49 209
        204 289
        2 380
        422 351
        101 326
        87 324
        366 404
        299 229
        367 336
        437 216
        218 269
        393 412
        238 89
        272 65
        219 131
        15 448
        240 414
        444 17
        287 429
        23 153
        337 231
        185 310
        355 247
        34 184
        237 363
        11 291
        18 366
        152 270
        303 118
        43 21
        156 262
        61 17
        386 137
        198 333
        108 347
        428 69
        62 221
        274 242
        417 29
        198 211
        168 368
        267 296
        125 374
        448 416
        422 297
        222 93
        57 140
        67 252
        0 26
        186 445
        103 83
        451 437
        90 120
        78 129
        234 416
        278 140
        144 10
        4 419
        32 208
        203 275
        182 441
        154 117
        400 258
        118 426
        206 171
        272 37
        338 157
        422 248
        329 372
        182 118
        423 249
        438 384
        416 105
        34 374
        136 10
        196 94
        177 210
        313 379
        282 419
        342 330
        161 27
        377 314
        36 164
        454 340
        6 52
        67 47
        365 410
        109 242
        422 392
        180 83
        48 25
        365 311
        62 429
        250 275
        410 91
        133 445
        240 40
        317 239
        43 49
        68 63
        319 28
        143 331
        214 149
        199 439
        91 268
        427 258
        1 191
        257 188
        100 325
        419 317
        190 79
        295 146
        404 260
        81 298
        226 381
        92 239
        371 232
        156 183
        295 45
        327 205
        328 260
        124 53
        84 318
        212 20
        442 379
        18 392
        359 297
        104 432
        142 223
        115 73
        141 276
        201 278
        376 150
        380 187
        164 19
        64 431
        278 127
        346 138
        235 159
        400 302
        343 301
        31 46
        385 294
        38 351
        8 373
        160 150
        216 303
        283 147
        220 323
        437 107
        426 358
        355 290
        41 347
        160 170
        200 330
        207 441
        193 112
        451 122
        282 92
        389 50
        401 271
        200 288
        280 407
        332 357
        59 191
        325 170
        156 273
        87 277
        376 167
        249 292
        334 199
        405 50
        328 21
        60 289
        360 159
        9 243
        27 231
        178 20
        38 78
        253 287
        321 239
        74 294
        31 134
        349 105
        29 453
        149 166
        387 306
        255 343
        339 248
        92 86
        330 93
        261 311
        415 46
        320 151
        194 445
        109 356
        307 390
        213 47
        316 215
        283 63
        167 259
        76 65
        319 353
        142 286
        367 160
        329 379
        41 438
        38 145
        67 406
        452 171
        230 351
        117 52
        53 120
        198 285
        197 285
        109 212
        71 22
        340 392
        344 89
        304 362
        284 314
        175 324
        22 353
        287 215
        366 174
        102 86
        123 63
        447 131
        361 205
        425 151
        11 202
        37 176
        143 115
        399 80
        254 41
        406 70
        295 94
        256 364
        22 348
        27 383
        420 61
        361 122
        111 382
        85 276
        388 114
        229 231
        277 269
        361 169
        315 372
        334 111
        208 406
        308 411
        360 39
        234 80
        420 314
        68 13
        168 201
        8 300
        206 310
        339 150
        31 84
        123 341
        169 129
        327 137
        108 121
        100 82
        433 275
        428 209
        257 134
        403 277
        238 345
        315 442
        57 310
        235 139
        77 239
        3 414
        435 181
        50 86
        120 196
        397 263
        223 259
        399 264
        197 55
        377 436
        87 373
        443 93
        441 85
        449 412
        185 181
        253 39
        255 448
        179 374
        36 326
        398 96
        """

        self.waters = """
        0.19206 0.60638 0.75
        0.80399 0.54001 0.65644
        0.0 0.47598 0.40606
        0.30399 0.04001 0.65644
        0.82101 0.93294 0.40405
        0.19422 0.36992 0.90861
        0.0 0.99645 0.125
        0.69206 0.75267 0.25
        0.0 0.04447 0.93549
        0.19601 0.54001 0.65644
        0.625 0.77197 0.93534
        0.0 0.8833 0.68549
        0.5 0.3833 0.68549
        0.375 0.06261 0.75
        0.0 0.86515 0.31049
        0.31706 0.67455 0.95379
        0.875 0.27197 0.56466
        0.18078 0.09854 0.15173
        0.19601 0.45999 0.15644
        0.68078 0.40146 0.65173
        0.68294 0.61226 0.65845
        0.32101 0.56707 0.90405
        0.18078 0.78925 0.75
        0.19422 0.5898 0.25
        0.19422 0.63008 0.40861
        0.81706 0.82545 0.04622
        0.125 0.56261 0.75
        0.625 0.88521 0.00255
        0.18078 0.83275 0.92122
        0.0 0.3605 0.65591
        0.19206 0.28583 0.43966
        0.30794 0.85975 0.40621
        0.0 0.48169 0.59125
        0.30578 0.0898 0.25
        0.30794 0.14025 0.59379
        0.625 0.05049 0.25
        0.875 0.44952 0.75
        0.31706 0.67455 0.54622
        0.19206 0.35975 0.40621
        0.0 0.17577 0.88913
        0.82101 0.06707 0.59595
        0.875 0.72803 0.43534
        0.18294 0.17455 0.54622
        0.19601 0.54001 0.84356
        0.375 0.11479 0.50255
        0.68078 0.59854 0.34827
        0.18294 0.88774 0.34155
        0.68294 0.38774 0.34155
        0.69206 0.85975 0.09379
        0.32101 0.50497 0.8125
        0.17899 0.93935 0.58923
        0.375 0.93739 0.25
        0.0 0.04092 0.06049
        0.5 0.54092 0.06049
        0.0 0.17577 0.61088
        0.69206 0.21417 0.56034
        0.0 0.48169 0.90875
        0.30794 0.85975 0.09379
        0.81706 0.76386 0.125
        0.80794 0.60638 0.75
        0.31922 0.28925 0.75
        0.30578 0.13008 0.09139
        0.30794 0.14025 0.90621
        0.5 0.02402 0.90606
        0.19422 0.30217 0.8567
        0.0 0.65697 0.65428
        0.81922 0.21075 0.25
        0.67899 0.43294 0.40405
        0.30399 0.04001 0.84356
        0.80399 0.54001 0.84356
        0.875 0.38521 0.49746
        0.19206 0.74733 0.75
        0.67899 0.43935 0.91077
        0.0 0.32119 0.68966
        0.81922 0.16725 0.42122
        0.5 0.82119 0.68966
        0.0 0.70246 0.63898
        0.82101 0.00497 0.6875
        0.31706 0.32545 0.45379
        0.32101 0.43935 0.58923
        0.0 0.65697 0.84572
        0.125 0.44952 0.75
        0.5 0.45908 0.93952
        0.19601 0.57081 0.50471
        0.18294 0.82545 0.45379
        0.69422 0.13008 0.40861
        0.30399 0.96925 0.65375
        0.69601 0.07081 0.9953
        0.30578 0.86992 0.59139
        0.30399 0.03075 0.15375
        0.80399 0.53075 0.15375
        0.31922 0.66725 0.07879
        0.5 0.98169 0.59125
        0.80578 0.36992 0.90861
        0.5 0.6167 0.18549
        0.82101 0.93294 0.09595
        0.69601 0.95999 0.34356
        0.80399 0.46925 0.84625
        0.19422 0.63008 0.09139
        0.0 0.95554 0.06452
        0.5 0.45554 0.06452
        0.67899 0.50497 0.6875
        0.17899 0.00497 0.6875
        0.32101 0.56065 0.41077
        0.30578 0.80217 0.8567
        0.80794 0.71417 0.93966
        0.5 0.49645 0.375
        0.18078 0.21075 0.25
        0.68294 0.67455 0.54622
        0.875 0.61479 0.50255
        0.0 0.54233 0.50269
        0.875 0.55049 0.25
        0.5 0.66117 0.36088
        0.30794 0.75267 0.25
        0.875 0.72803 0.06466
        0.80578 0.30217 0.6433
        0.0 0.16117 0.36088
        0.17899 0.06065 0.08923
        0.18078 0.09854 0.34827
        0.875 0.43739 0.25
        0.67899 0.56065 0.08923
        0.5 0.67577 0.61088
        0.625 0.22803 0.43534
        0.5 0.98169 0.90875
        0.5 0.54447 0.93549
        0.30794 0.10638 0.75
        0.31922 0.40146 0.65173
        0.0 0.86515 0.18952
        0.81922 0.78925 0.75
        0.5 0.32424 0.38913
        0.80578 0.63008 0.09139
        0.81922 0.90146 0.84827
        0.31922 0.71075 0.25
        0.31706 0.73614 0.625
        0.375 0.88521 0.49746
        0.125 0.27197 0.93534
        0.69206 0.78583 0.06034
        0.0 0.27343 0.25
        0.80794 0.74733 0.75
        0.30794 0.24733 0.75
        0.18294 0.82545 0.04622
        0.5 0.11525 0.25
        0.5 0.28676 0.17136
        0.68078 0.33275 0.57879
        0.375 0.77197 0.93534
        0.125 0.38521 0.49746
        0.31922 0.59854 0.34827
        0.625 0.06261 0.75
        0.81922 0.16725 0.07879
        0.30399 0.03075 0.34625
        0.19601 0.42919 0.00471
        0.80399 0.53075 0.34625
        0.625 0.22803 0.06466
        0.31922 0.59854 0.15173
        0.30399 0.07081 0.9953
        0.80399 0.57081 0.9953
        0.69206 0.14025 0.59379
        0.18078 0.90146 0.84827
        0.68078 0.71075 0.25
        0.30794 0.21417 0.93966
        0.0 0.45767 0.00269
        0.375 0.88521 0.00255
        0.82101 0.93935 0.91077
        0.5 0.88475 0.75
        0.80578 0.4102 0.75
        0.5 0.04233 0.50269
        0.375 0.05049 0.25
        0.19206 0.35975 0.09379
        0.18294 0.76386 0.125
        0.5 0.28676 0.32864
        0.80399 0.42919 0.00471
        0.30399 0.92919 0.00471
        0.0 0.63559 0.75
        0.5 0.13559 0.75
        0.5 0.49645 0.125
        0.69601 0.03075 0.15375
        0.19206 0.71417 0.56034
        0.81922 0.83275 0.57879
        0.67899 0.56707 0.59595
        0.17899 0.06707 0.59595
        0.125 0.61479 0.50255
        0.5 0.86442 0.25
        0.0 0.1167 0.31452
        0.625 0.11479 0.50255
        0.5 0.15697 0.65428
        0.30794 0.89362 0.25
        0.5 0.71324 0.82864
        0.19601 0.53075 0.34625
        0.69422 0.86992 0.59139
        0.0 0.00355 0.625
        0.19601 0.42919 0.4953
        0.875 0.56261 0.75
        0.5 0.97598 0.09394
        0.5 0.6896 0.25
        0.68294 0.73614 0.625
        0.5 0.36515 0.31049
        0.68078 0.59854 0.15173
        0.5 0.20246 0.63898
        0.18294 0.23614 0.625
        0.0 0.61525 0.25
        0.5 0.33884 0.86088
        0.0 0.78676 0.17136
        0.18078 0.90146 0.65173
        0.82101 0.99503 0.3125
        0.68078 0.28925 0.75
        0.80794 0.28583 0.43966
        0.17899 0.93294 0.09595
        0.69422 0.0898 0.25
        0.0 0.45767 0.49731
        0.5 0.50355 0.875
        0.69422 0.80217 0.6433
        0.0 0.21324 0.67136
        0.80794 0.64025 0.59379
        0.80794 0.35975 0.40621
        0.5 0.01831 0.40875
        0.81706 0.11226 0.84155
        0.18078 0.16725 0.42122
        0.5 0.84304 0.34572
        0.81922 0.09854 0.15173
        0.69422 0.9102 0.75
        0.82101 0.06065 0.41077
        0.18294 0.11226 0.84155
        0.875 0.38521 0.00255
        0.5 0.32424 0.11088
        0.67899 0.49503 0.1875
        0.30578 0.9102 0.75
        0.81706 0.23614 0.875
        0.5 0.20246 0.86102
        0.0 0.78676 0.32864
        0.81922 0.83275 0.92122
        0.32101 0.43294 0.40405
        0.69422 0.86992 0.90861
        0.80794 0.35975 0.09379
        0.68294 0.73614 0.875
        0.80794 0.64025 0.90621
        0.18294 0.23614 0.875
        0.19601 0.46925 0.65375
        0.31922 0.33275 0.57879
        0.5 0.01831 0.09125
        0.69601 0.96925 0.65375
        0.69601 0.04001 0.65644
        0.0 0.52402 0.90606
        0.80578 0.63008 0.40861
        0.0 0.52402 0.59394
        0.18294 0.76386 0.375
        0.0 0.21324 0.82864
        0.0 0.83884 0.63913
        0.19206 0.28583 0.06034
        0.31706 0.38774 0.15845
        0.5 0.50355 0.625
        0.0 0.95554 0.43549
        0.31922 0.66725 0.42122
        0.5 0.45554 0.43549
        0.81706 0.17455 0.95379
        0.81706 0.76386 0.375
        0.5 0.63485 0.81049
        0.69601 0.95999 0.15644
        0.625 0.88521 0.49746
        0.0 0.00355 0.875
        0.31706 0.32545 0.04622
        0.32101 0.56065 0.08923
        0.0 0.67882 0.18966
        0.81706 0.11226 0.65845
        0.19206 0.71417 0.93966
        0.31706 0.61226 0.84155
        0.5 0.54092 0.43952
        0.0 0.04092 0.43952
        0.0 0.67882 0.31034
        0.19422 0.69783 0.1433
        0.69422 0.13008 0.09139
        0.69422 0.19783 0.1433
        0.5 0.45908 0.56049
        0.19206 0.64025 0.59379
        0.81706 0.17455 0.54622
        0.0 0.6395 0.34409
        0.0 0.99645 0.375
        0.5 0.1395 0.34409
        0.625 0.11479 0.99746
        0.0 0.82424 0.11088
        0.125 0.61479 0.99746
        0.0 0.54233 0.99731
        0.5 0.22658 0.75
        0.5 0.95767 0.49731
        0.69601 0.04001 0.84356
        0.375 0.22803 0.06466
        0.30794 0.21417 0.56034
        0.68294 0.26386 0.125
        0.69206 0.14025 0.90621
        0.31922 0.33275 0.92122
        0.5 0.31041 0.75
        0.19206 0.25267 0.25
        0.81922 0.90146 0.65173
        0.5 0.54447 0.56452
        0.5 0.36515 0.18952
        0.69422 0.19783 0.3567
        0.5 0.6167 0.31452
        0.19422 0.69783 0.3567
        0.0 0.36442 0.25
        0.19601 0.46925 0.84625
        0.69422 0.80217 0.8567
        0.17899 0.06707 0.90405
        0.67899 0.56707 0.90405
        0.69601 0.96925 0.84625
        0.30578 0.13008 0.40861
        0.81706 0.23614 0.625
        0.81706 0.88774 0.15845
        0.5 0.77343 0.25
        0.69206 0.89362 0.25
        0.0 0.1896 0.25
        0.80794 0.28583 0.06034
        0.18294 0.88774 0.15845
        0.80578 0.69783 0.1433
        0.68294 0.38774 0.15845
        0.81706 0.82545 0.45379
        0.30578 0.19783 0.1433
        0.375 0.77197 0.56466
        0.0 0.13485 0.81049
        0.82101 0.93935 0.58923
        0.18078 0.83275 0.57879
        0.0 0.83884 0.86088
        0.67899 0.49503 0.3125
        0.625 0.94952 0.75
        0.875 0.27197 0.93534
        0.69601 0.07081 0.50471
        0.82101 0.06065 0.08923
        0.67899 0.43294 0.09595
        0.80399 0.46925 0.65375
        0.0 0.29754 0.36102
        0.19601 0.57081 0.9953
        0.5 0.79754 0.36102
        0.68078 0.33275 0.92122
        0.80578 0.36992 0.59139
        0.31706 0.61226 0.65845
        0.125 0.27197 0.56466
        0.80578 0.5898 0.25
        0.30399 0.95999 0.15644
        0.80399 0.45999 0.15644
        0.5 0.8605 0.84409
        0.30578 0.86992 0.90861
        0.32101 0.43294 0.09595
        0.19601 0.45999 0.34356
        0.30399 0.96925 0.84625
        0.80578 0.30217 0.8567
        0.68294 0.61226 0.84155
        0.17899 0.99503 0.1875
        0.5 0.04233 0.99731
        0.0 0.72658 0.75
        0.80794 0.71417 0.56034
        0.30578 0.80217 0.6433
        0.0 0.70246 0.86102
        0.69206 0.10638 0.75
        0.31706 0.38774 0.34155
        0.875 0.61479 0.99746
        0.0 0.81041 0.75
        0.125 0.72803 0.43534
        0.31706 0.26386 0.125
        0.80399 0.57081 0.50471
        0.5 0.63485 0.68952
        0.30399 0.07081 0.50471
        0.80794 0.39362 0.25
        0.18294 0.17455 0.95379
        0.68294 0.26386 0.375
        0.69206 0.24733 0.75
        0.5 0.33884 0.63913
        0.82101 0.99503 0.1875
        0.68078 0.66725 0.07879
        0.32101 0.49503 0.1875
        0.0 0.47598 0.09394
        0.30794 0.78583 0.06034
        0.30399 0.95999 0.34356
        0.80399 0.45999 0.34356
        0.0 0.34304 0.15428
        0.30794 0.78583 0.43966
        0.82101 0.06707 0.90405
        0.18294 0.11226 0.65845
        0.68294 0.32545 0.45379
        0.125 0.38521 0.00255
        0.5 0.17882 0.18966
        0.5 0.8605 0.65591
        0.69206 0.78583 0.43966
        0.0 0.51831 0.40875
        0.69206 0.21417 0.93966
        0.125 0.55049 0.25
        0.69601 0.92919 0.00471
        0.68078 0.66725 0.42122
        0.5 0.17882 0.31034
        0.0 0.29754 0.13898
        0.5 0.79754 0.13898
        0.125 0.72803 0.06466
        0.0 0.95908 0.56049
        0.625 0.93739 0.25
        0.0 0.34304 0.34572
        0.125 0.43739 0.25
        0.19422 0.4102 0.75
        0.69206 0.85975 0.40621
        0.32101 0.56707 0.59595
        0.32101 0.43935 0.91077
        0.31706 0.73614 0.875
        0.5 0.97598 0.40606
        0.19206 0.64025 0.90621
        0.82101 0.00497 0.8125
        0.67899 0.43935 0.58923
        0.81706 0.88774 0.34155
        0.375 0.11479 0.99746
        0.19601 0.53075 0.15375
        0.30399 0.92919 0.4953
        0.80399 0.42919 0.4953
        0.0 0.51831 0.09125
        0.0 0.82424 0.38913
        0.0 0.04447 0.56452
        0.5 0.66117 0.13913
        0.0 0.16117 0.13913
        0.31922 0.40146 0.84827
        0.0 0.13485 0.68952
        0.5 0.02402 0.59394
        0.17899 0.93294 0.40405
        0.68294 0.67455 0.95379
        0.19422 0.36992 0.59139
        0.69601 0.03075 0.34625
        0.69601 0.92919 0.4953
        0.18078 0.16725 0.07879
        0.17899 0.93935 0.91077
        0.19206 0.39362 0.25
        0.32101 0.50497 0.6875
        0.31706 0.26386 0.375
        0.67899 0.56065 0.41077
        0.17899 0.06065 0.41077
        0.17899 0.00497 0.8125
        0.67899 0.50497 0.8125
        0.5 0.15697 0.84572
        0.68294 0.32545 0.04622
        0.0 0.32119 0.81034
        0.5 0.82119 0.81034
        0.17899 0.99503 0.3125
        0.0 0.95908 0.93952
        0.5 0.84304 0.15428
        0.5 0.1395 0.15591
        0.30578 0.19783 0.3567
        0.80578 0.69783 0.3567
        0.0 0.6395 0.15591
        0.19422 0.30217 0.6433
        0.81922 0.09854 0.34827
        0.625 0.77197 0.56466
        0.0 0.3605 0.84409
        0.0 0.1167 0.18549
        0.5 0.71324 0.67136
        0.375 0.94952 0.75
        0.0 0.8833 0.81452
        0.5 0.67577 0.88913
        0.5 0.3833 0.81452
        0.68078 0.40146 0.84827
        0.375 0.22803 0.43534
        0.5 0.95767 0.00269
        0.0 0.38475 0.75
        0.32101 0.49503 0.3125
        0.80794 0.25267 0.25
        """

        self.coord = "relative"

        self.cages = """
        12 0.0 0.42107 -0.11499
        12 0.0 0.57893 0.38501
        15 0.0 -0.1139 -0.50806
        12 0.0 0.32408 -0.00864
        12 -0.5 -0.17592 -0.00864
        12 0.0 0.42107 0.61499
        15 0.0 -0.1139 1.00806
        12 0.5 0.9096 0.12575
        15 1.0 0.93604 0.25
        15 0.5 0.6139 0.50806
        16 0.5 0.72762 0.06456
        14 -0.26825 -0.31923 0.75
        16 0.5 0.27238 -0.06456
        12 0.0 0.32408 0.50864
        15 0.5 0.43604 0.25
        12 -0.22313 0.15157 0.25
        12 0.5 0.99431 0.25
        12 -0.5 -0.07893 0.61499
        14 -0.21597 0.0 0.5
        12 0.5 0.17592 0.00864
        14 0.21597 0.0 0.0
        14 0.26825 -0.31923 -0.25
        12 0.5 0.9096 0.37425
        12 0.0 -0.49431 0.75
        12 0.5 0.2362 0.25
        12 0.0 -0.4096 -0.12575
        12 -0.22313 -0.15157 0.75
        16 0.5 0.72762 0.43544
        15 0.0 0.04977 0.25
        12 -0.5 -0.07893 -0.11499
        14 0.71597 0.5 -0.5
        14 -0.26825 0.31923 0.25
        15 0.5 0.45023 0.75
        15 0.0 -0.04977 0.75
        12 0.0 -0.4096 0.62575
        12 -0.5 -0.17592 0.50864
        12 0.72313 0.65157 0.25
        15 0.5 0.3861 1.00806
        16 0.0 -0.22762 -0.06456
        12 -0.5 0.07893 0.38501
        14 0.28403 0.5 0.5
        14 0.26825 0.31923 0.25
        14 0.76825 0.18077 -0.25
        12 0.0 0.4096 0.12575
        12 0.22313 -0.15157 -0.25
        12 0.0 0.67592 0.49136
        15 -0.5 -0.43604 0.75
        16 0.0 0.22762 0.06456
        14 -0.21597 0.0 0.0
        14 0.23175 0.18077 0.75
        14 0.23175 0.81923 0.25
        15 0.0 0.1139 -0.00806
        12 -0.5 -0.2362 0.75
        12 -0.5 0.17592 0.49136
        12 1.0 0.67592 0.00864
        12 0.0 0.4096 0.37425
        12 0.0 0.2638 0.75
        14 0.76825 0.81923 0.25
        15 0.5 0.3861 -0.50806
        15 0.5 0.6139 -0.00806
        14 0.71597 0.5 0.0
        12 0.5 0.07893 0.11499
        12 1.0 0.7362 0.25
        12 0.5 0.00569 0.75
        12 0.72313 0.34843 -0.25
        12 0.5 0.0904 -0.12575
        12 0.27687 0.34843 0.75
        15 0.0 0.06396 0.75
        15 0.5 0.54977 0.25
        16 0.0 0.22762 0.43544
        14 0.28403 0.5 0.0
        12 1.0 0.57893 0.11499
        14 0.21597 0.0 -0.5
        16 0.0 -0.22762 0.56456
        15 0.0 0.1139 0.50806
        12 0.5 0.0904 0.62575
        12 0.27687 0.65157 0.25
        12 0.0 0.49431 0.25
        12 0.22313 0.15157 0.25
        16 0.5 0.27238 0.56456
        """

        self.bondlen = 3

        self.cell = """
        14.660858880484453 73.8382409300653 26.369216077228458
        """

        self.density = 0.47748377898764377

        self.cell = cellvectors(a=14.660858880484453,
                                b=73.8382409300653,
                                c=26.369216077228458)
