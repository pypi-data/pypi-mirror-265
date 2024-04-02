from ._animation import PWNAnimation, np
from ..._math import PWNVector, _PWNAnimationDataPlaceholder


class SetCoordsAnimation(PWNAnimation):
    def __init__(self, obj, coords1, anim_time=-1):
        if type(obj) != str:
            coords0 = self._get_data0(obj)
            self._setup_method(obj)
        else:
            coords0 = []
        if type(coords1) == PWNVector:
            coords1 = _PWNAnimationDataPlaceholder(None, None, coords1)
        PWNAnimation.__init__(self, obj,
                              np.array(coords0),
                              np.array(coords1) if (type(coords1) != _PWNAnimationDataPlaceholder) and (coords1 is not None) else coords1,
                              anim_time)
        self.set_coord = None
        self.prev_coords = []

    def animate_step(self):
        if len(self._data0) == 0:
            self._data0 = np.array(self._get_data0(self.mut_obj))
        if self._data1 is None:
            self._data1 = np.empty((0, 3)) # [[]] * len(self._data0[0])
        if self.set_coord is None:
            self._setup_method(self.mut_obj)

        if self._progress >= self._N - 1:
            self.set_coord(self._data1)
            return  # self._data1
        if type(self._data1) == _PWNAnimationDataPlaceholder and self._data1.data1_vect is not None:
            self._data1 = self._data0 + self._data1.data1_vect.xy

        new_coords = self._get_prog_data()
        self.prev_coords += [new_coords]
        self.set_coord(new_coords)
        self._progress += 1

    def _setup_method(self, obj):
        if getattr(obj, "set_xy", None):
            self.set_coord = lambda c: obj.set_xy(c)
        elif getattr(obj, "set_center", None):
            self.set_coord = lambda c: obj.set_center(c)
        elif getattr(obj, "set_position", None):
            self.set_coord = lambda c: obj.set_position(c)
        elif getattr(obj, "set_offsets", None):
            self.set_coord = lambda c: obj.set_offsets(c)
        elif getattr(obj, "_offsets3d", None):
            def set_offsets3d(c):
                obj._offsets3d = c.T
            self.set_coord = set_offsets3d
        elif getattr(obj, "set_data", None):
            if self._data0.shape[1] == 2:
                def set_linedata2d(c):
                    obj.set_data(*c.T)
                self.set_coord = set_linedata2d
            else:
                def set_linedata3d(c):
                    obj.set_data(*c.T[:2])
                    obj.set_3d_properties(c.T[2])
                self.set_coord = set_linedata3d
        else:
            raise Exception("Not implemented yet!")

    def _get_data0(self, obj):
        if getattr(obj, "get_xy", None):
            return obj.get_xy()
        elif getattr(obj, "get_center", None):
            return obj.get_center()
        elif getattr(obj, "get_position", None):
            return obj.get_position()
        elif getattr(obj, "get_offsets", None):
            data0 = np.array(obj.get_offsets())
            if getattr(obj, "_offsets3d", None):
                data0 = np.hstack((data0, np.array(obj._offsets3d).reshape((-1,1))))
            return data0
        elif getattr(obj, "get_data_3d", None):
            return np.array(obj.get_data_3d()).T
        elif getattr(obj, "get_data", None):
            return np.array(obj.get_data()).T
        else:
            # print(obj)
            raise Exception("Not implemented for class" + str(obj.__class__))
