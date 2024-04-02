from ._animation import PWNAnimation, np


class SetTextAnimation(PWNAnimation):
    def __init__(self, obj, new_text, anim_time=-1):
        if type(obj) != str:
            text0 = self._get_data0(obj)
        else:
            text0 = []
        PWNAnimation.__init__(self, obj,
                              text0,
                              new_text,
                              anim_time)

    def animate_step(self):
        if self._progress >= self._N - 1:
            self.mut_obj.set_text(self._data1)
            return  # self._data1
        if len(self._data0) == 0:
            self._data0 = self._get_data0(self.mut_obj)

        new_text = self._get_prog_data()
        self.mut_obj.set_text(new_text)

        self._progress += 1

    def _get_prog_data(self):
        t = self._progress / self._N
        if t < 0.5:
            symb_lim = np.floor((0.5 - t) * 2 * len(self._data0)).astype(int)
            return self._data0[:symb_lim]
        else:
            symb_lim = np.ceil((t - 0.5) * 2 * len(self._data1)).astype(int)
            return self._data1[:symb_lim]

    def _get_data0(self, obj):
        return obj.get_text()
