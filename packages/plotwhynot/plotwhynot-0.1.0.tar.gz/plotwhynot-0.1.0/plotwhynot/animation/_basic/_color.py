from ._animation import PWNAnimation, np
from matplotlib.colors import to_rgb


class SetColorAnimation(PWNAnimation):
    def __init__(self, obj, rgb1, anim_time=-1):
        if type(obj) != str:
            rgb0 = self._get_data0(obj)
        else:
            rgb0 = []
        # rgb0 = self._get_data0(obj)
        if type(rgb1) == str:
            rgb1 = to_rgb(rgb1)
        PWNAnimation.__init__(self, obj,
                              np.array(rgb0),
                              np.array(rgb1) if "function" not in str(type(rgb1)) else rgb1,
                              anim_time)

    def setup(self):
        self._data0 = self._get_data0(self.mut_obj)

    def animate_step(self):
        if self._progress >= self._N - 1:
            self.mut_obj.set_color(self._data1)
            return  # self._data1
        if len(self._data0) == 0:
            self._data0 = self._get_data0(self.mut_obj)
        if "function" in str(type(self._data1)):
            self._data1 = self._data1()
            if type(self._data1) == str:
                self._data1 = np.array(to_rgb(self._data1))

        new_color = self._get_prog_data()
        self.mut_obj.set_color(new_color)
        self._progress += 1

    def _get_data0(self, obj):
        clr = None
        if getattr(obj, "get_facecolor", None):
            clr = obj.get_facecolor()
        elif getattr(obj, "get_color", None):
            clr = obj.get_color()
        else:
            raise Exception("Unknown get_color method for class" + str(obj.__class__))
        if type(clr) == str:
            return to_rgb(clr)
        else:
            return np.reshape(clr, -1)[:3]
