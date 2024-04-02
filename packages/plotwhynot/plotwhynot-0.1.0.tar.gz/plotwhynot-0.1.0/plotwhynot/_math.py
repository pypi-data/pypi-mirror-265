import numpy as _np


class PWNVector:
    def __init__(self, vect_coords):
        self.xy = _np.array(vect_coords)


class _PWNAnimationDataPlaceholder:
    def __init__(self, data0=None, data1=None, data1vect=None):
        self.data0 = data0
        self.data1 = data1
        self.data1_vect = data1vect
