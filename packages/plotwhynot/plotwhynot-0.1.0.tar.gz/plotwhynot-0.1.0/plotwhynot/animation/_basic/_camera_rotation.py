from ._animation import PWNAnimation, np


class RotateCameraAnimation(PWNAnimation):
    def __init__(self, ax, tgt_rotation, anim_time=-1):
        if type(ax) != str:
            rot0 = self._get_data0(ax)
        else:
            rot0 = []
        PWNAnimation.__init__(self,
                              ax,
                              rot0,
                              np.array(tgt_rotation),
                              anim_time)

    def animate_step(self):
        if self._progress >= self._N - 1:
            self.mut_obj.view_init(elev=self._data1[0],
                                   azim=self._data1[1])
            self._progress += 1
            return

        if len(self._data0) == 0:
            self._data0 = self._get_data0(self.mut_obj)

        new_elev, new_azim = self._get_prog_data()
        self.mut_obj.view_init(elev=new_elev,
                               azim=new_azim)
        self._progress += 1

    def _get_data0(self, obj):
        return np.array([obj.elev, obj.azim])
