from ._animation import PWNAnimation, np
from ..._math import PWNVector, _PWNAnimationDataPlaceholder


class RotateAnimation(PWNAnimation):
    def __init__(self, obj, angle, center=None, anim_time=-1):
        if type(obj) != str:
            self.points0 = self._get_coords0(obj)
            self._setup_method(obj)
        else:
            self.points0 = []
            self.set_coord = None
        self.center = np.array(center) if center is not None else center
        PWNAnimation.__init__(self, obj,
                              np.array([0]),
                              np.array([angle]) / 180 * np.pi,
                              anim_time)

    def animate_step(self):
        if len(self.points0) == 0:
            self.points0 = np.array(self._get_coords0(self.mut_obj))
        if self.center is None:
            self.center = self.points0.mean(axis=0)
        if self.set_coord is None:
            self._setup_method(self.mut_obj)

        if self._progress >= self._N - 1:
            phi = self._data1[0]
            M = np.array([[np.cos(phi), -np.sin(phi)],
                          [np.sin(phi), np.cos(phi)]])
            new_pts = (M @ (self.points0 - self.center).T).T + self.center
            self.set_coord(new_pts)
            return

        phi = self._get_prog_data()[0]
        M = np.array([[np.cos(phi),  -np.sin(phi)],
                      [np.sin(phi), np.cos(phi)]])
        new_pts = (M @ (self.points0 - self.center).T).T + self.center
        self.set_coord(new_pts)
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
            if self.points0.shape[1] == 2:
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

    def _get_coords0(self, obj):
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
