from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from ..._utils._constants import _ANIMATION_STEP_TIME, _DEFAULT_ANIMATION_TIME


class PWNAnimation:
    def __init__(self, mut_obj, data0, data1, anim_time=-1):
        self._data0 = data0
        self._data1 = data1
        self.mut_obj = mut_obj
        if anim_time < 0:
            anim_time = _DEFAULT_ANIMATION_TIME

        self._N = anim_time // _ANIMATION_STEP_TIME
        self._progress = 1

    def animate_step(self):
        raise NotImplementedError("Must be overridden!")

    def _get_prog_data(self):
        # MARK: linear animation. May be overridden for custom performance
        # print(self._data0, self._data1)
        t = self._progress / (self._N - 1)
        return (1 - t) * np.array(self._data0) + t * np.array(self._data1)

    def _get_data0(self, obj):
        raise NotImplementedError("Must be overridden!")

    def setup(self):
        pass

    def copy(self):
        return deepcopy(self)


class PWNAnimationGroup:
    def __init__(self, figure, animations, duration, interval, next_actions=None, prev_act_results=None):
        self.fig = figure
        self.animations = animations
        self.interval = interval
        self.N = np.ceil(duration / interval).astype(int) + 1
        self.next_actions = next_actions
        self.prev_act_results = prev_act_results
        self._anim = None
        self.exception = None
        self.shared_data = {}
        self.i_s = []
        self.exception = None
        self.log = []

    def start(self):
        self._anim = FuncAnimation(self.fig,
                                   self.update,
                                   np.arange(1, self.N),
                                   init_func=self.setup,
                                   interval=self.interval,
                                   blit=True)
        plt.show()

    def setup(self):
        self.log += ["setup started"]
        for anim in self.animations:
            anim.setup()

        self.log += ["setup over"]
        self.log += [[anim.mut_obj for anim in self.animations]]
        return [anim.mut_obj for anim in self.animations]

    def update(self, i):
        self.log += ["upd started"]
        self.i_s = self.i_s + [i]
        try:
            for anim in self.animations:
                anim.animate_step()
            if i == self.N - 1:
                self._anim.event_source.stop()
                if self.next_actions is not None:
                    self._run_following_actions()
        except Exception as e:
            self.shared_data["exception"] = e
        return  # [anim._mut_obj for anim in self.animations]

    def to_gif(self):
        # TODO: extend to following actions
        FuncAnimation(self.fig,
                      self.update,
                      np.arange(1, self.N),
                      init_func=self.setup,
                      interval=self.interval,
                      blit=True).save('./animation.gif', writer='imagemagick', fps=30)

    def _run_following_actions(self):
        i = 0
        ax = self.shared_data["plt_results"]["ax"]
        while i < len(self.next_actions) and "anim" not in self.next_actions[i][0]:
            if self.next_actions[i][0] == "func":
                _, func = self.next_actions[i]
                args = [self.shared_data]
                kwargs = {}
                plt_method = "func"
            else:
                plt_method, args, kwargs = self.next_actions[i]

            try:
                if plt_method == "func":
                    app_actions = func(self.shared_data)
                    if app_actions is not None:
                        self.next_actions = self.next_actions[:i + 1] + app_actions + self.next_actions[i + 1:]
                else:
                    act_res = getattr(super(ax.__class__, ax), plt_method)(*args, **kwargs)
                    n_prev_acts = len([act for act in self.shared_data["plt_results"] if plt_method in act])
                    self.shared_data["plt_results"][f"{plt_method}_{n_prev_acts}"] = act_res
            except Exception as e:
                self.shared_data["exception"] = e
                raise e
            i += 1

        if i == len(self.next_actions):
            return

        act_name, _, anim_grp_action = self.next_actions[i]
        anim_grp_action.fig = self.fig
        for anim in anim_grp_action.animations:
            if "sleep" in str(anim.__class__).lower():
                continue
            obj = self.shared_data["plt_results"][anim.mut_obj]
            if type(obj) in [tuple, list]:
                obj = obj[0]
            anim.mut_obj = obj
        anim_grp_action.next_actions = self.next_actions[i + 1:]
        anim_grp_action.shared_data = self.shared_data

        anim_grp_action.start()
