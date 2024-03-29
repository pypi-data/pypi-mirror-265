from genice2.cell import cellvectors
import genice2.lattices

desc = {"ref": {"EMT(a)": "Liu 2019",
                "EMT(b)": 'IZA Database'},
        "usage": "No options available.",
        "brief": "Hypothetical ice with a large cavity."
        }


class Lattice(genice2.lattices.Lattice):
    def __init__(self):
        self.cell = cellvectors(a=15.621810598341442,
                                b=15.621810598341442,
                                c=25.483106896463806,
                                C=120.0)

        self.waters = [
            [0.15499999999999936, 0.6664999999999992, 0.30429999999999957],
            [0.3335000000000008, 0.48850000000000016, 0.30429999999999957],
            [0.5114999999999998, 0.8450000000000006, 0.30429999999999957],
            [0.8450000000000006, 0.3335000000000008, 0.8042999999999996],
            [0.6664999999999992, 0.5114999999999998, 0.8042999999999996],
            [0.48850000000000016, 0.15499999999999936, 0.8042999999999996],
            [0.3335000000000008, 0.8450000000000006, 0.30429999999999957],
            [0.5114999999999998, 0.6664999999999992, 0.30429999999999957],
            [0.15499999999999936, 0.48850000000000016, 0.30429999999999957],
            [0.6664999999999992, 0.15499999999999936, 0.8042999999999996],
            [0.48850000000000016, 0.3335000000000008, 0.8042999999999996],
            [0.8450000000000006, 0.5114999999999998, 0.8042999999999996],
            [0.8450000000000006, 0.3335000000000008, 0.6957000000000004],
            [0.6664999999999992, 0.5114999999999998, 0.6957000000000004],
            [0.48850000000000016, 0.15499999999999936, 0.6957000000000004],
            [0.15499999999999936, 0.6664999999999992, 0.19570000000000043],
            [0.3335000000000008, 0.48850000000000016, 0.19570000000000043],
            [0.5114999999999998, 0.8450000000000006, 0.19570000000000043],
            [0.6664999999999992, 0.15499999999999936, 0.6957000000000004],
            [0.48850000000000016, 0.3335000000000008, 0.6957000000000004],
            [0.8450000000000006, 0.5114999999999998, 0.6957000000000004],
            [0.3335000000000008, 0.8450000000000006, 0.19570000000000043],
            [0.5114999999999998, 0.6664999999999992, 0.19570000000000043],
            [0.15499999999999936, 0.48850000000000016, 0.19570000000000043],
            [0.15559999999999974, 0.6671999999999993, 0.5708000000000002],
            [0.33280000000000065, 0.4884000000000004, 0.5708000000000002],
            [0.5115999999999996, 0.8444000000000003, 0.5708000000000002],
            [0.8444000000000003, 0.33280000000000065, 0.0708000000000002],
            [0.6671999999999993, 0.5115999999999996, 0.0708000000000002],
            [0.4884000000000004, 0.15559999999999974, 0.0708000000000002],
            [0.33280000000000065, 0.8444000000000003, 0.5708000000000002],
            [0.5115999999999996, 0.6671999999999993, 0.5708000000000002],
            [0.15559999999999974, 0.4884000000000004, 0.5708000000000002],
            [0.6671999999999993, 0.15559999999999974, 0.0708000000000002],
            [0.4884000000000004, 0.33280000000000065, 0.0708000000000002],
            [0.8444000000000003, 0.5115999999999996, 0.0708000000000002],
            [0.8444000000000003, 0.33280000000000065, 0.4291999999999998],
            [0.6671999999999993, 0.5115999999999996, 0.4291999999999998],
            [0.4884000000000004, 0.15559999999999974, 0.4291999999999998],
            [0.15559999999999974, 0.6671999999999993, 0.9291999999999998],
            [0.33280000000000065, 0.4884000000000004, 0.9291999999999998],
            [0.5115999999999996, 0.8444000000000003, 0.9291999999999998],
            [0.6671999999999993, 0.15559999999999974, 0.4291999999999998],
            [0.4884000000000004, 0.33280000000000065, 0.4291999999999998],
            [0.8444000000000003, 0.5115999999999996, 0.4291999999999998],
            [0.33280000000000065, 0.8444000000000003, 0.9291999999999998],
            [0.5115999999999996, 0.6671999999999993, 0.9291999999999998],
            [0.15559999999999974, 0.4884000000000004, 0.9291999999999998],
            [0.09639999999999915, 0.7262999999999984, 0.48210000000000086],
            [0.2737000000000016, 0.37010000000000076, 0.48210000000000086],
            [0.6298999999999992, 0.9036000000000008, 0.48210000000000086],
            [0.9036000000000008, 0.2737000000000016, 0.9821000000000009],
            [0.7262999999999984, 0.6298999999999992, 0.9821000000000009],
            [0.37010000000000076, 0.09639999999999915, 0.9821000000000009],
            [0.2737000000000016, 0.9036000000000008, 0.48210000000000086],
            [0.6298999999999992, 0.7262999999999984, 0.48210000000000086],
            [0.09639999999999915, 0.37010000000000076, 0.48210000000000086],
            [0.7262999999999984, 0.09639999999999915, 0.9821000000000009],
            [0.37010000000000076, 0.2737000000000016, 0.9821000000000009],
            [0.9036000000000008, 0.6298999999999992, 0.9821000000000009],
            [0.9036000000000008, 0.2737000000000016, 0.5178999999999991],
            [0.7262999999999984, 0.6298999999999992, 0.5178999999999991],
            [0.37010000000000076, 0.09639999999999915, 0.5178999999999991],
            [0.09639999999999915, 0.7262999999999984, 0.01789999999999914],
            [0.2737000000000016, 0.37010000000000076, 0.01789999999999914],
            [0.6298999999999992, 0.9036000000000008, 0.01789999999999914],
            [0.7262999999999984, 0.09639999999999915, 0.5178999999999991],
            [0.37010000000000076, 0.2737000000000016, 0.5178999999999991],
            [0.9036000000000008, 0.6298999999999992, 0.5178999999999991],
            [0.2737000000000016, 0.9036000000000008, 0.01789999999999914],
            [0.6298999999999992, 0.7262999999999984, 0.01789999999999914],
            [0.09639999999999915, 0.37010000000000076, 0.01789999999999914],
            [0.036599999999999966, 0.6069999999999993, 0.39250000000000007],
            [0.3930000000000007, 0.42960000000000065, 0.39250000000000007],
            [0.5703999999999994, 0.9634, 0.39250000000000007],
            [0.9634, 0.3930000000000007, 0.8925000000000001],
            [0.6069999999999993, 0.5703999999999994, 0.8925000000000001],
            [0.42960000000000065, 0.036599999999999966, 0.8925000000000001],
            [0.3930000000000007, 0.9634, 0.39250000000000007],
            [0.5703999999999994, 0.6069999999999993, 0.39250000000000007],
            [0.036599999999999966, 0.42960000000000065, 0.39250000000000007],
            [0.6069999999999993, 0.036599999999999966, 0.8925000000000001],
            [0.42960000000000065, 0.3930000000000007, 0.8925000000000001],
            [0.9634, 0.5703999999999994, 0.8925000000000001],
            [0.9634, 0.3930000000000007, 0.6074999999999999],
            [0.6069999999999993, 0.5703999999999994, 0.6074999999999999],
            [0.42960000000000065, 0.036599999999999966, 0.6074999999999999],
            [0.036599999999999966, 0.6069999999999993, 0.10749999999999993],
            [0.3930000000000007, 0.42960000000000065, 0.10749999999999993],
            [0.5703999999999994, 0.9634, 0.10749999999999993],
            [0.6069999999999993, 0.036599999999999966, 0.6074999999999999],
            [0.42960000000000065, 0.3930000000000007, 0.6074999999999999],
            [0.9634, 0.5703999999999994, 0.6074999999999999],
            [0.3930000000000007, 0.9634, 0.10749999999999993],
            [0.5703999999999994, 0.6069999999999993, 0.10749999999999993],
            [0.036599999999999966, 0.42960000000000065, 0.10749999999999993],
        ]
        self.coord = "relative"
        self.bondlen = 3
        self.density = 0.5327914455045754
