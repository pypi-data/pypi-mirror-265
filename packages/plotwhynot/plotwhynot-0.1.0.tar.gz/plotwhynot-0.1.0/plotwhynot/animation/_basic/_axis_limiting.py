from ._animation import PWNAnimation, np


class SetAxisLimitsAnimation(PWNAnimation):
    def __init__(self, ax, axis, limits, anim_time=-1):
        self.axis = axis
        if type(ax) != str:
            limits0 = self._get_data0(ax)
            self._setup_method(ax, axis)
        else:
            limits0 = []
            self.set_limits = None

        super().__init__(ax,
                         np.array(limits0),
                         np.array(limits),
                         anim_time)

    def animate_step(self):
        if self.set_limits is None:
            self._setup_method(self.mut_obj, self.axis)
        if self._progress >= self._N - 1:
            self.set_limits(self._data1)
            return
        if len(self._data0) == 0:
            self._data0 = np.array(self._get_data0(self.mut_obj))
        new_limits = self._get_prog_data()
        self.set_limits(new_limits)
        self._progress += 1

    def _setup_method(self, ax, axis):
        if axis not in ["x", "y", "z"]:
            raise ValueError("Axis must be x, y or z!")

        self.set_limits = ax.set_xlim if axis == "x" else (ax.set_ylim if axis == "y" else ax.set_zlim)

    def _get_data0(self, ax):
        if self.axis not in ["x", "y", "z"]:
            raise ValueError("Axis must be x, y or z!")

        if self.axis == "x":
            return np.array(ax.get_xlim())
        elif self.axis == "y":
            return np.array(ax.get_ylim())
        else:
            return np.array(ax.get_zlim())
