import matplotlib.pyplot as _plt
from mpl_toolkits.mplot3d import Axes3D as _Axes3D
from matplotlib.axes import Axes as _Axes2D
from ._utils._protocol import _ScenePlayProtocol


class PWNAxes(_Axes2D, _ScenePlayProtocol):
    def __init__(self, *args, **kwargs):
        # if len(args) == 1 and (isinstance(args[0], plt.Axes) or isinstance(args[0], PWNAxes)):
        #     super().__init__(args[0].get_figure(), args[0]._position)
        #     self._init_animations()
        #     return
        self._actions = []
        self._shared_data = {"ax": self,
                             "plt_results": {"ax": self},
                             "data": {}}

        super().__init__(*([args[0]] + [[0.1, 0.1, 0.75, 0.75]] + list(args[1:])), **kwargs)
        self._shared_data["fig"] = self.get_figure()
        self.axis("equal")

    def scatter(self, *args, **kwargs):
        return self._add_plot_action("scatter", *args, **kwargs)

    def plot(self, *args, **kwargs):
        return self._add_plot_action("plot", *args, **kwargs)

    def add_patch(self, p, **kwargs):
        return self._add_plot_action("add_patch", *[p], **kwargs)

    def hist(self, *args, **kwargs):
        return self._add_plot_action("hist", *args, **kwargs)

    def text(self, *args, **kwargs):
        return self._add_plot_action("text", *args, **kwargs)

    def play(self):
        i = 0
        while i < len(self._actions) and self._actions[i][0] != "anim":
            if self._actions[i][0] == "func":
                app_actions = self._actions[i][1](self._shared_data)
                if app_actions is not None:
                    self._actions = self._actions[:i + 1] + app_actions + self._actions[i+1:]
            else:
                plt_method, args, kwargs = self._actions[i]
                act_res = getattr(super(), plt_method)(*args, **kwargs)
                n_prev_acts = len([act for act in self._shared_data["plt_results"] if plt_method in act])
                self._shared_data["plt_results"][f"{plt_method}_{n_prev_acts}"] = act_res
            i += 1

        if i == len(self._actions):
            return
        act_name, _, anim_grp_action = self._actions[i]
        anim_grp_action.fig = self.figure
        for anim in anim_grp_action.animations:
            if "sleep" in str(anim.__class__).lower():
                continue
            # obj = act_results[anim.mut_obj]
            obj = self._shared_data["plt_results"][anim.mut_obj]
            if type(obj) in [tuple, list]:
                obj = obj[-1]

            # TODO: manage hist

            # print("\t", obj)
            anim.mut_obj = obj
            # print("\t\t", anim.mut_obj)
        anim_grp_action.next_actions = self._actions[i + 1:]
        # anim_grp_action.prev_act_results = act_results
        anim_grp_action.shared_data = self._shared_data

        anim_grp_action.start()
        # plt.show()

    # def to_gif(self):

    def inspect_exception(self):
        if "exception" in self._shared_data:
            raise self._shared_data["exception"]

    def __getitem__(self, item):
        for key_grp in ["plt_results", "data"]:
            if item in self._shared_data[key_grp]:
                return self._shared_data[key_grp][item]
        raise KeyError


class PWNAxes3D(_Axes3D, _ScenePlayProtocol):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and (isinstance(args[0], _plt.Axes) or isinstance(args[0], PWNAxes)):
            super().__init__(args[0].get_figure(), args[0]._position)
            self._init_animations()
            return
        self._actions = []
        self._shared_data = {"ax": self,
                             "plt_results": {"ax": self},
                             "data": {}}

        super().__init__(*args, **kwargs)
        self._shared_data["fig"] = self.get_figure()
        self.axis("auto")

    def scatter(self, *args, **kwargs):
        return self._add_plot_action("scatter", *args, **kwargs)

    def plot(self, *args, **kwargs):
        return self._add_plot_action("plot", *args, **kwargs)

    def add_patch(self, p, **kwargs):
        return self._add_plot_action("add_patch", *[p], **kwargs)

    def text(self, *args, **kwargs):
        return self._add_plot_action("text", *args, **kwargs)

    def play(self):
        i = 0
        while i < len(self._actions) and self._actions[i][0] != "anim":
            if self._actions[i][0] == "func":
                app_actions = self._actions[i][1](self._shared_data)
                if app_actions is not None:
                    self._actions = self._actions[:i + 1] + app_actions + self._actions[i+1:]
            else:
                plt_method, args, kwargs = self._actions[i]
                act_res = getattr(super(), plt_method)(*args, **kwargs)
                n_prev_acts = len([act for act in self._shared_data["plt_results"] if plt_method in act])
                self._shared_data["plt_results"][f"{plt_method}_{n_prev_acts}"] = act_res
            i += 1

        if i == len(self._actions):
            return
        act_name, _, anim_grp_action = self._actions[i]
        anim_grp_action.fig = self.figure
        for anim in anim_grp_action.animations:
            if "sleep" in str(anim.__class__).lower():
                continue
            # obj = act_results[anim.mut_obj]
            obj = self._shared_data["plt_results"][anim.mut_obj]
            if type(obj) in [tuple, list]:
                obj = obj[0]
            # print("\t", obj)
            anim.mut_obj = obj
            # print("\t\t", anim.mut_obj)
        anim_grp_action.next_actions = self._actions[i + 1:]
        anim_grp_action.shared_data = self._shared_data

        anim_grp_action.start()
        # plt.show()

    def inspect_exception(self):
        if "exception" in self._shared_data:
            raise self._shared_data["exception"]

    def __getitem__(self, item):
        for key_grp in ["plt_results", "data"]:
            if item in self._shared_data[key_grp]:
                return self._shared_data[key_grp][item]
        raise KeyError
