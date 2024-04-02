from ._animation import PWNAnimation, np


class DrawLineAnimation(PWNAnimation):
    def __init__(self, mut_obj, *coords, anim_time=-1):
        super().__init__(mut_obj, np.array([c[0] for c in coords]),
                         np.array([c[-1] for c in coords]), anim_time)
        self.points = np.array(coords).T
        part_lens = np.array([np.linalg.norm(self.points[i] - self.points[i - 1])
                              for i in range(1, len(self.points))])
        self.rel_cum_lens = np.cumsum([0] + part_lens.tolist())[:-1] / sum(part_lens)

    def animate_step(self):
        if self._progress >= self._N - 1:
            coords = self.points.T
        else:
            coords = self._get_prog_data()
        if len(coords) == 2:
            self.mut_obj.set_data(*coords)
        else:
            self.mut_obj.set_data_3d(*coords)
        self._progress += 1

    def _get_data0(self, obj):
        pass

    def _get_prog_data(self):
        if self._progress >= self._N - 1:
            return self.points[:, 0], self.points[:, 1]

        t = self._progress / (self._N - 1)
        cur_part_ind = np.where(t >= self.rel_cum_lens)[0][-1]

        pts = self.points[:cur_part_ind + 1]

        t = (t - self.rel_cum_lens[cur_part_ind]) / np.linalg.norm(self.points[cur_part_ind] - self.points[cur_part_ind + 1])

        pts = np.vstack((pts,
                         (1 - t) * self.points[cur_part_ind] + t * self.points[cur_part_ind + 1]
                         ))

        return pts.T
