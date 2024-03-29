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
        260 21
        310 120
        134 7
        1 284
        0 295
        157 55
        268 239
        97 107
        68 123
        4 237
        64 89
        43 280
        246 168
        87 261
        216 298
        321 138
        2 31
        6 251
        281 200
        287 217
        114 224
        75 247
        16 222
        132 25
        144 320
        112 105
        285 82
        251 50
        4 150
        253 318
        64 14
        90 235
        208 275
        102 195
        69 224
        3 126
        106 176
        29 139
        226 249
        237 121
        142 171
        254 211
        219 174
        147 235
        20 115
        304 191
        190 305
        122 278
        141 237
        312 94
        184 29
        259 38
        285 272
        103 238
        178 208
        43 8
        126 31
        250 47
        45 202
        56 20
        321 82
        270 271
        99 121
        168 208
        99 211
        79 18
        307 35
        293 95
        65 137
        181 93
        246 205
        242 243
        218 27
        106 205
        20 182
        121 7
        307 41
        257 70
        192 300
        23 138
        153 195
        24 167
        176 61
        103 160
        0 223
        223 212
        228 261
        306 303
        76 112
        225 125
        86 146
        19 299
        286 212
        175 90
        131 46
        218 317
        113 142
        175 246
        220 298
        104 123
        314 32
        304 42
        88 73
        188 307
        241 79
        23 70
        11 53
        286 170
        10 222
        24 80
        178 45
        35 151
        138 207
        107 277
        60 169
        276 148
        38 310
        297 127
        321 80
        257 18
        14 171
        172 100
        145 117
        215 233
        73 226
        143 168
        232 215
        300 249
        227 170
        244 238
        185 46
        206 282
        287 29
        242 44
        272 145
        4 159
        259 196
        85 131
        146 158
        153 315
        93 32
        23 76
        260 169
        161 31
        16 54
        161 159
        236 234
        69 117
        104 101
        11 202
        214 284
        14 254
        50 296
        315 230
        261 191
        273 124
        189 145
        189 147
        128 209
        24 225
        106 214
        256 34
        28 310
        177 259
        240 199
        228 252
        65 71
        87 32
        286 245
        87 52
        133 275
        295 105
        274 135
        77 57
        116 297
        39 150
        255 91
        250 158
        164 271
        239 266
        200 318
        172 171
        206 291
        198 308
        230 295
        265 152
        316 130
        237 169
        47 80
        299 210
        2 184
        258 134
        116 28
        95 17
        223 267
        224 267
        268 226
        183 219
        182 219
        165 301
        43 266
        100 322
        172 125
        214 101
        188 274
        256 59
        274 34
        240 201
        40 162
        263 257
        262 191
        218 160
        165 215
        119 89
        270 121
        79 139
        28 261
        269 137
        180 99
        12 285
        250 42
        53 311
        51 140
        263 170
        64 234
        114 78
        50 129
        190 143
        131 321
        81 240
        270 111
        265 292
        58 109
        14 21
        318 13
        65 115
        238 254
        295 66
        113 125
        86 49
        193 201
        254 290
        229 60
        217 120
        308 124
        119 128
        306 129
        45 227
        163 27
        128 130
        197 296
        118 163
        97 56
        293 18
        126 231
        260 150
        184 105
        289 79
        198 67
        110 91
        9 94
        220 137
        3 116
        148 48
        3 54
        304 48
        167 30
        93 213
        90 124
        68 166
        180 296
        192 70
        11 218
        181 52
        2 38
        78 139
        3 38
        130 282
        308 83
        154 84
        244 197
        30 194
        236 221
        143 185
        144 186
        36 95
        12 205
        110 232
        191 66
        177 120
        236 185
        309 183
        319 41
        108 60
        245 267
        136 98
        216 182
        62 34
        67 311
        197 298
        288 252
        162 21
        197 15
        198 15
        9 234
        84 48
        111 141
        33 173
        13 151
        229 282
        232 108
        319 159
        86 82
        164 194
        294 233
        36 49
        323 159
        207 289
        247 173
        11 221
        200 35
        6 264
        222 173
        213 22
        257 207
        259 210
        140 37
        125 30
        181 291
        180 238
        179 72
        286 83
        2 59
        279 37
        269 78
        236 160
        314 36
        272 49
        147 245
        102 83
        198 50
        95 245
        75 305
        166 148
        178 85
        315 47
        190 164
        209 53
        225 279
        133 149
        319 141
        166 297
        217 17
        23 285
        77 154
        189 224
        260 301
        96 136
        118 46
        314 22
        309 293
        269 278
        74 275
        144 171
        277 193
        281 323
        216 289
        244 279
        86 90
        19 135
        168 131
        9 280
        71 205
        12 122
        204 203
        244 118
        271 312
        112 151
        318 127
        155 98
        27 219
        280 89
        152 233
        78 313
        137 235
        81 25
        228 135
        267 292
        24 140
        199 155
        258 44
        109 156
        162 63
        253 266
        242 72
        144 92
        104 42
        199 149
        42 284
        26 256
        190 306
        32 17
        41 157
        49 147
        119 204
        263 178
        63 55
        192 112
        311 155
        231 117
        116 252
        132 174
        85 207
        96 193
        251 311
        193 247
        98 201
        84 66
        157 92
        132 317
        74 221
        132 322
        34 165
        320 58
        225 46
        81 179
        232 239
        67 202
        157 8
        281 10
        200 231
        277 305
        102 220
        265 69
        141 282
        162 89
        158 36
        111 316
        186 156
        287 18
        320 55
        5 229
        37 149
        294 154
        297 231
        273 167
        126 323
        187 305
        138 315
        5 280
        186 316
        97 187
        241 104
        192 287
        67 149
        100 186
        227 183
        217 249
        300 13
        302 7
        57 252
        293 170
        203 72
        180 302
        5 136
        91 288
        235 83
        213 117
        199 290
        177 283
        85 163
        298 115
        152 291
        296 303
        76 230
        302 187
        122 145
        51 56
        37 15
        241 309
        10 8
        209 317
        246 82
        202 275
        113 164
        40 44
        19 109
        206 283
        51 214
        167 174
        265 93
        255 33
        274 58
        111 92
        264 322
        33 201
        181 307
        110 57
        1 47
        134 173
        255 108
        255 109
        26 151
        114 184
        268 233
        303 115
        222 91
        40 150
        1 195
        69 31
        103 204
        177 226
        129 124
        35 213
        309 158
        113 185
        256 105
        283 52
        72 134
        62 77
        228 62
        313 289
        229 239
        58 301
        248 148
        106 208
        139 123
        94 8
        63 43
        273 183
        322 30
        281 41
        299 283
        100 81
        263 176
        223 84
        320 21
        127 57
        276 70
        161 39
        189 269
        319 291
        165 39
        187 303
        294 292
        96 9
        304 68
        59 39
        156 243
        216 163
        195 212
        71 278
        172 290
        76 22
        169 211
        130 243
        317 204
        262 314
        73 13
        301 108
        290 279
        308 227
        16 323
        119 242
        142 234
        179 33
        87 120
        52 135
        136 53
        10 253
        215 77
        62 66
        313 153
        210 44
        146 80
        6 194
        96 221
        262 230
        59 196
        175 65
        248 154
        45 27
        209 264
        210 54
        6 270
        73 266
        248 127
        302 203
        20 101
        278 123
        97 25
        248 300
        19 288
        88 26
        75 271
        176 276
        292 17
        51 133
        12 276
        273 146
        75 7
        143 74
        88 63
        102 15
        247 94
        118 160
        272 22
        5 128
        1 140
        101 71
        179 156
        133 107
        166 122
        299 243
        203 25
        288 54
        220 313
        61 48
        264 316
        188 26
        152 161
        129 194
        240 107
        74 277
        40 196
        61 212
        98 60
        310 29
        28 68
        294 249
        103 64
        241 182
        56 174
        188 55
        110 253
        268 206
        0 153
        155 211
        88 196
        312 92
        251 99
        4 258
        142 312
        16 258
        175 306
        250 262
        61 284
        0 114
        """

        self.waters = """
        0.28445 0.68534 0.27187
        0.45825 0.66439 0.1069
        0.08256 0.66629 0.41701
        0.91105 0.72171 0.45724
        0.16622 0.82886 0.63068
        0.71035 0.17115 0.70202
        0.38276 0.12879 0.83561
        0.05076 0.84914 0.76587
        0.0088 0.13953 0.63914
        0.92436 0.18599 0.74735
        0.9546 0.02785 0.59083
        0.7295 0.17252 0.89352
        0.95996 0.02869 0.20833
        0.92459 0.19928 0.43436
        0.20578 0.53534 0.75555
        0.33927 0.78509 0.01181
        0.95658 0.81418 0.5849
        0.55418 0.21491 0.32152
        0.79387 0.33561 0.22643
        0.60596 0.55697 0.56083
        0.83378 0.66264 0.03599
        0.21491 0.55418 0.67848
        0.24208 0.24801 0.3091
        0.07542 0.2747 0.2323
        0.39329 0.47667 0.01542
        0.73469 0.59975 0.85935
        0.13495 0.40026 0.47399
        0.78509 0.33927 0.98819
        0.75791 0.6289 0.35693
        0.91662 0.52333 0.31792
        0.41628 0.33372 0.91633
        0.15115 0.82566 0.43278
        0.47125 0.29845 0.35326
        0.70382 0.77709 0.70961
        0.35174 0.61462 0.4728
        0.15086 0.20163 0.43254
        0.44302 0.2705 0.22685
        0.41551 0.70919 0.98679
        0.92487 0.6018 0.43397
        0.25152 0.74572 0.52078
        0.03401 0.56239 0.60754
        0.20163 0.15086 0.56746
        0.62197 0.62001 0.1927
        0.92673 0.22291 0.62372
        0.92386 0.5913 0.62701
        0.70155 0.1728 0.01993
        0.12901 0.3711 0.9764
        0.38801 0.52325 0.14089
        0.64024 0.83763 0.26382
        0.30368 0.15726 0.20061
        0.32119 0.96159 0.93094
        0.64661 0.73014 0.01587
        0.50153 0.37397 0.47516
        0.6227 0.12851 0.83521
        0.85357 0.69632 0.53394
        0.1974 0.35977 0.59716
        0.73014 0.64661 0.98413
        0.69632 0.85357 0.46606
        0.40367 0.56255 0.60772
        0.13524 0.61199 0.47423
        0.52333 0.91662 0.68208
        0.61903 0.87304 0.18972
        0.46466 0.67045 0.42221
        0.03842 0.35961 0.59761
        0.04899 0.44303 0.77251
        0.04343 0.8576 0.08177
        0.44582 0.66074 0.34515
        0.52838 0.96599 0.94087
        0.77709 0.70382 0.29039
        0.22291 0.92673 0.37628
        0.91773 0.20998 0.2499
        0.93082 0.84158 0.12431
        0.83763 0.64024 0.73618
        0.87121 0.25397 0.50228
        0.8576 0.04343 0.91823
        0.02869 0.95996 0.79167
        0.17115 0.33737 0.29734
        0.55698 0.82748 0.43981
        0.07513 0.67693 0.2327
        0.86477 0.47676 0.19244
        0.33372 0.41628 0.08367
        0.62001 0.62197 0.8073
        0.14825 0.18874 0.1257
        0.39404 0.95101 0.10584
        0.52875 0.8272 0.3134
        0.96159 0.32119 0.06906
        0.2783 0.18935 0.12391
        0.56255 0.40367 0.39228
        0.99804 0.37803 0.52603
        0.95207 0.40855 0.70613
        0.26163 0.07564 0.08068
        0.73838 0.81401 0.58598
        0.24801 0.24208 0.6909
        0.35977 0.1974 0.40285
        0.9966 0.11168 0.71497
        0.53534 0.20578 0.24445
        0.81066 0.08895 0.79057
        0.79002 0.70775 0.91657
        0.58373 0.91744 0.75034
        0.26531 0.86505 0.80732
        0.49974 0.50125 0.80661
        0.80072 0.7253 0.10103
        0.32956 0.79422 0.08888
        0.0 0.50302 0.83333
        0.74603 0.61724 0.16895
        0.16692 0.52133 0.36462
        0.79838 0.94924 0.0992
        0.7253 0.80072 0.89897
        0.5392 0.82885 0.63132
        0.54352 0.59145 0.6272
        0.72171 0.91105 0.54276
        0.33737 0.17115 0.70266
        0.08354 0.3534 0.34921
        0.18935 0.2783 0.87609
        0.17115 0.71035 0.29798
        0.99408 0.75199 0.02424
        0.81401 0.73838 0.41401
        0.13953 0.0088 0.36086
        0.04793 0.45648 0.96053
        0.84113 0.43746 0.72561
        0.71555 0.40088 0.3948
        0.20998 0.91773 0.7501
        0.97215 0.92674 0.2575
        0.84885 0.67451 0.23389
        0.3711 0.12901 0.0236
        0.32307 0.3982 0.89937
        0.04049 0.85176 0.45903
        0.81418 0.95658 0.41511
        0.68534 0.28445 0.72813
        0.29618 0.07327 0.95706
        0.58449 0.29368 0.67988
        0.07327 0.29618 0.04295
        0.66439 0.45825 0.8931
        0.66264 0.83378 0.96401
        0.95035 0.77693 0.71007
        0.49698 0.49698 0.5
        0.67693 0.07513 0.7673
        0.14643 0.84275 0.13273
        0.12879 0.38276 0.16439
        0.91744 0.58373 0.24966
        0.47867 0.64559 0.03129
        0.3534 0.08354 0.6508
        0.15726 0.30368 0.7994
        0.0034 0.11508 0.9517
        0.33256 0.4087 0.70632
        0.11168 0.9966 0.28503
        0.3982 0.32307 0.10063
        0.30385 0.02692 0.2017
        0.77693 0.95035 0.28993
        0.52535 0.8098 0.9379
        0.19021 0.71555 0.60457
        0.08227 0.29225 0.41677
        0.37803 0.99804 0.47397
        0.25445 0.62547 0.18854
        0.5913 0.92386 0.37299
        0.47676 0.86477 0.80756
        0.57736 0.52906 0.68569
        0.17341 0.22307 0.62327
        0.50581 0.3773 0.16855
        0.19928 0.92459 0.56564
        0.95101 0.39404 0.89416
        0.25397 0.87121 0.49772
        0.04829 0.47094 0.64765
        0.95171 0.42265 0.01902
        0.18874 0.14825 0.87431
        0.37102 0.74555 0.52187
        0.86047 0.86927 0.3058
        0.47667 0.39329 0.98458
        0.99121 0.13074 0.02753
        0.35441 0.83308 0.69796
        0.62604 0.12757 0.14182
        0.2705 0.44302 0.77315
        0.3773 0.50581 0.83145
        0.86927 0.86047 0.69419
        0.64559 0.47867 0.96871
        0.11508 0.0034 0.0483
        0.74353 0.0 0.16667
        0.74555 0.37102 0.47813
        0.8026 0.16237 0.06951
        0.67881 0.64039 0.73572
        0.12696 0.74599 0.85639
        0.38098 0.25402 0.47694
        0.8098 0.52535 0.0621
        0.59912 0.31467 0.06146
        0.08338 0.60671 0.34875
        0.07564 0.26163 0.91932
        0.47162 0.43761 0.7258
        0.94924 0.79838 0.90079
        0.25402 0.38098 0.52306
        0.18599 0.92436 0.25265
        0.07326 0.04541 0.92417
        0.52906 0.57736 0.31431
        0.91646 0.26986 0.31746
        0.81126 0.95951 0.79236
        0.32549 0.17434 0.90056
        0.38538 0.73712 0.13947
        0.99848 0.49875 0.52672
        0.1728 0.70155 0.98007
        0.42265 0.95171 0.98098
        0.4942 0.74849 0.85411
        0.04005 0.06874 0.45833
        0.67451 0.84885 0.76611
        0.66744 0.07614 0.96035
        0.87304 0.61903 0.81028
        0.87243 0.49847 0.80849
        0.93126 0.97131 0.125
        0.54175 0.20614 0.55977
        0.00197 0.37999 0.14064
        0.82659 0.04966 0.0434
        0.62547 0.25445 0.81146
        0.82748 0.55698 0.56019
        0.33561 0.79387 0.77357
        0.49847 0.87243 0.19151
        0.22307 0.17341 0.37673
        0.70775 0.79002 0.08343
        0.49419 0.87149 0.49812
        0.96599 0.52838 0.05913
        0.70632 0.29081 0.34655
        0.79422 0.32956 0.91112
        0.70919 0.41551 0.01321
        0.17252 0.7295 0.10648
        0.84275 0.14643 0.86727
        0.88493 0.88832 0.61836
        0.43746 0.84113 0.27439
        0.24209 0.87099 0.30974
        0.28966 0.46081 0.96465
        0.74572 0.25152 0.47922
        0.59633 0.15887 0.05894
        0.55697 0.60596 0.43917
        0.60671 0.08338 0.65125
        0.28445 0.47465 0.27123
        0.02785 0.9546 0.40916
        0.6018 0.92487 0.56603
        0.49875 0.99848 0.47327
        0.02692 0.30385 0.7983
        0.27693 0.97308 0.13164
        0.97308 0.27693 0.86837
        0.26986 0.91646 0.68254
        0.12757 0.62604 0.85818
        0.66628 0.08256 0.58299
        0.61724 0.74603 0.83105
        0.74849 0.4942 0.14589
        0.8272 0.52875 0.6866
        0.66074 0.44582 0.65485
        0.15887 0.59633 0.94106
        0.44303 0.04899 0.22749
        0.04541 0.07326 0.07583
        0.92674 0.97215 0.7425
        0.75792 0.00593 0.35757
        0.71555 0.19021 0.39543
        0.50125 0.49974 0.19339
        0.37999 0.00197 0.85936
        0.69616 0.72308 0.46497
        0.85176 0.04049 0.54097
        0.26288 0.64826 0.80613
        0.6289 0.75791 0.64307
        0.20614 0.54175 0.44023
        0.86505 0.26531 0.19268
        0.00593 0.75792 0.64243
        0.87149 0.49419 0.50188
        0.29081 0.70632 0.65345
        0.59145 0.54352 0.3728
        0.43761 0.47162 0.27421
        0.74599 0.12696 0.14361
        0.5058 0.25429 0.81256
        0.35961 0.03842 0.40239
        0.82566 0.15115 0.56722
        0.40855 0.95207 0.29387
        0.61199 0.13524 0.52577
        0.08895 0.81066 0.20943
        0.2747 0.07542 0.7677
        0.15842 0.08924 0.79097
        0.18583 0.1424 0.25156
        0.46081 0.28966 0.03535
        0.37397 0.50153 0.52484
        0.75199 0.99408 0.97576
        0.84914 0.05076 0.23413
        0.84158 0.93082 0.87569
        0.95951 0.81126 0.20764
        0.31467 0.59912 0.93854
        0.87099 0.24209 0.69026
        0.06874 0.04005 0.54167
        0.52133 0.16692 0.63538
        0.61462 0.35174 0.5272
        0.59975 0.73469 0.14065
        0.08924 0.15842 0.20903
        0.50302 0.0 0.16667
        0.83308 0.35441 0.30205
        0.72308 0.69616 0.53503
        0.00152 0.50027 0.13994
        0.37454 0.62899 0.8552
        0.40026 0.13495 0.52602
        0.47094 0.04829 0.35236
        0.64826 0.26288 0.19387
        0.56239 0.03401 0.39246
        0.29368 0.58449 0.32012
        0.16237 0.8026 0.93049
        0.88832 0.88493 0.38163
        0.07614 0.66744 0.03965
        0.67045 0.46466 0.57779
        0.82886 0.16622 0.36932
        0.40088 0.71555 0.6052
        0.0 0.74353 0.83333
        0.04966 0.82659 0.9566
        0.64039 0.67881 0.26428
        0.97131 0.93126 0.875
        0.13074 0.99121 0.97247
        0.25647 0.25647 0.5
        0.45648 0.04793 0.03947
        0.62898 0.37454 0.1448
        0.82885 0.53919 0.36869
        0.50027 0.00152 0.86006
        0.1424 0.18583 0.74844
        0.12851 0.6227 0.16479
        0.4087 0.33256 0.29368
        0.25429 0.5058 0.18744
        0.47465 0.28445 0.72877
        0.73712 0.38538 0.86053
        0.91077 0.06919 0.45764
        0.29225 0.08227 0.58324
        0.29845 0.47125 0.64674
        0.17434 0.32549 0.09945
        0.52325 0.38801 0.85911
        0.06919 0.91077 0.54236
        """

        self.coord = "relative"

        self.cages = """
        12 -0.29724 -0.47143 1.4628433333333335
        12 -0.29659 0.05056 0.46721666666666667
        12 -0.34715 -0.05056 0.8661166666666668
        14 0.41127 -0.05384 1.5931033333333335
        12 -0.05056 -0.34715 -0.8661166666666668
        16 0.08828 -0.33415 1.7301533333333334
        12 0.17419 0.47143 -0.12951
        12 0.22991 -0.10768 -0.9734566666666667
        12 -0.54679 -0.33608 0.22888666666666668
        12 -0.10768 0.22991 0.9734566666666667
        12 0.54679 0.21071 0.43778
        15 -0.23604 0.0 0.6666666666666667
        12 -0.33608 -0.54679 1.7711133333333335
        12 0.0 0.10912 0.8333366666666667
        16 -0.54702 -0.33352 0.7283366666666667
        14 -0.05384 0.41127 0.40689666666666663
        15 0.0 0.11477 0.33333
        15 -0.11477 -0.11477 0.9999966666666668
        12 -0.22053 -0.17176 0.19667666666666667
        12 -0.33759 -0.22991 0.3598766666666666
        12 0.29659 0.34715 0.19945
        15 0.23604 0.23604 0.0
        16 -0.42243 -0.08828 1.0634866666666667
        14 0.46511 0.05384 -0.25977
        14 -0.41127 -0.46511 -0.9264366666666667
        12 0.21071 0.54679 -0.43778
        16 0.33352 -0.2135 1.3950033333333334
        15 0.0 -0.23604 1.3333333333333335
        15 0.11477 0.0 -0.33333
        16 0.2135 0.54702 0.06167
        12 -0.17419 0.29724 0.7961766666666668
        12 0.05056 -0.29659 1.5327833333333334
        16 -0.33352 -0.54702 -0.7283366666666667
        12 0.10912 0.0 0.16667
        12 0.33759 0.10768 0.30679
        16 0.54702 0.2135 -0.06167
        12 0.34715 0.29659 -0.19945
        12 0.10768 0.33759 -0.30679
        12 -0.17176 -0.22053 1.8033233333333334
        16 0.42243 0.33415 -0.39682
        14 -0.46511 -0.41127 0.9264366666666667
        14 0.05384 0.46511 0.25977
        12 -0.21071 0.33608 1.1044466666666668
        12 -0.22991 -0.33759 1.6401233333333334
        12 0.33608 -0.21071 -1.1044466666666668
        12 0.17176 -0.04877 -1.1366566666666666
        12 0.47143 0.17419 0.12951
        12 -0.10912 -0.10912 1.5000033333333334
        12 0.22053 0.04877 0.46999
        16 -0.08828 -0.42243 -1.0634866666666667
        12 -0.04877 0.17176 1.1366566666666666
        12 0.04877 0.22053 -0.46999
        12 0.29724 -0.17419 -0.7961766666666668
        16 -0.2135 0.33352 0.6049966666666666
        12 -0.47143 -0.29724 0.5371566666666666
        16 0.33415 0.42243 0.39682
        16 -0.33415 0.08828 0.2698466666666667
        """

        self.bondlen = 3

        self.cell = """
        23.11522320014082 0.0 0.0
        -11.557611600070405 20.01837050546938 0.0
        2.4223392964645325e-15 4.1956147346472185e-15 39.559802845213156
        """

        self.density = 0.5290489188846392

        self.cell = cellvectors(a=23.11522320014082,
                                b=23.11522320014082,
                                c=39.559802845213156,
                                C=119.99999999999999)
