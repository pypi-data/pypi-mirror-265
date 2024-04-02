from ..animation import *
from ..animation._basic._animation import PWNAnimationGroup
from ._utils import *
from ._grouping import PWNPlotBlock
from ._constants import _ANIMATION_STEP_TIME, _DEFAULT_ANIMATION_TIME
from matplotlib.patches import Rectangle
import numpy as np


class _ScenePlayProtocol:
    def add_custom_action(self, func):
        n_prev_actions = len([v for v in self._actions if v[0] == "func"])
        plt_result_key = f"func_{n_prev_actions}"
        self._actions += [("func", func)]

    def create_group(self, *elem_ids):
        n_prev_grps = len([v for v in self._shared_data["plt_results"] if "grp" in v])
        tgt_key = f"grp_{n_prev_grps}"
        self._shared_data["plt_results"][tgt_key] = PWNPlotBlock(elem_ids)
        return tgt_key

    def merge_animations(self, *anim_ids):
        raise NotImplementedError("Will be supported later!")
        # TODO: merge all anims in one animation group
        # TODO: check if animations are not split by plots / custom actions
        # TODO: remove old animations
        # TODO: add new animation
        # TODO: return new anim id
        pass

    def _add_plot_action(self, method_name, *args, **kwargs):
        n_prev_actions = len([v for v in self._actions if v[0] == method_name])
        plt_result_key = f"{method_name}_{n_prev_actions}"

        if "animated" in kwargs or "anim_time" in kwargs:
            if "anim_time" in kwargs and "animated" not in kwargs:
                kwargs["animated"] = True
            anim_time = 1000
            if "anim_time" in kwargs:
                anim_time = kwargs["anim_time"]

            if kwargs["animated"] != False:
                if method_name == "plot":
                    if kwargs["animated"] == True:
                        kwargs["animated"] = "draw"
                    if kwargs["animated"] == "draw":
                        kwargs = dict_no_animated_key(kwargs)
                        self._actions += [(method_name, [[coord[0]] * len(coord) for coord in args], kwargs)]
                        # data_key = get_plot_method_key(method_name, "data")
                        self.add_animation(DrawLineAnimation(plt_result_key,
                                                             *args,
                                                             anim_time=anim_time)
                                           )
                    elif kwargs["animated"] == "appear":
                        color_key = get_plot_method_key(method_name, "color")
                        if color_key in kwargs:
                            tgt_color = kwargs[color_key]
                        else:
                            tgt_color = "blue"
                        kwargs[color_key] = "white"
                        kwargs = dict_no_animated_key(kwargs)

                        n_bins = kwargs["bins"] if "bins" in kwargs else args[1] if len(args) > 1 else 5
                        bin_heights = np.histogram(args[0], bins=n_bins)  # TODO: range?

                        self._actions += [(method_name, args, kwargs)]
                        self.add_animation(ScaleAnimation(plt_result_key,
                                                          anim_time=anim_time,
                                                          height=bin_heights)
                                           )
                    else:
                        raise ValueError("No such animation type for plot!")
                elif method_name == "add_patch":
                    # TODO: support different types of patches!
                    if type(args[0]) is not Rectangle:
                        raise NotImplementedError("Only rects supported by now!")

                    if kwargs["animated"] == True:
                        kwargs["animated"] = "appear"
                    if kwargs["animated"] == "appear":
                        # color_key = get_plot_method_key(method_name, "color")
                        tgt_color = args[0].get_facecolor()[:3]
                        args[0].set_facecolor("white")
                        kwargs = dict_no_animated_key(kwargs)
                        self._actions += [(method_name, args, kwargs)]
                        self.add_animation(SetColorAnimation(plt_result_key, tgt_color,
                                                             anim_time)
                                           )
                    elif kwargs["animated"] in ["center", "corner"]:
                        corner, w, h = args[0].get_xy(), args[0].get_width(), args[0].get_height()
                        c = np.array(corner) + np.array([w,h]) / 2

                        if kwargs["animated"] == "center":
                            args[0].set_xy(c)
                        args[0].set_width(0)
                        args[0].set_height(0)

                        appear_anims = [ScaleAnimation(plt_result_key,
                                                       width=w,
                                                       height=h,
                                                       anim_time=anim_time)]
                        if kwargs["animated"] == "center":
                            appear_anims = [SetCoordsAnimation(plt_result_key,
                                                               corner,
                                                               anim_time)] + appear_anims
                        kwargs = dict_no_animated_key(kwargs)
                        self._actions += [(method_name, args, kwargs)]
                        self.add_animation(*appear_anims)
                        # self.add_animation(PWNAnimationGroup(self.get_figure(),
                        #                                      appear_anims,
                        #                                      anim_time,
                        #                                      ANIMATION_STEP_TIME)
                        #                    )
                    else:
                        raise ValueError("No such animation!")
                elif method_name == "scatter":
                    if kwargs["animated"] == True:
                        kwargs["animated"] = "appear"
                    if kwargs["animated"] == "appear":
                        color_key = get_plot_method_key(method_name, "color")
                        if color_key in kwargs:
                            tgt_color = kwargs[color_key]
                        else:
                            tgt_color = "blue"
                        kwargs[color_key] = "white"
                        kwargs = dict_no_animated_key(kwargs)
                        self._actions += [(method_name, args, kwargs)]
                        self.add_animation(SetColorAnimation(plt_result_key, tgt_color, anim_time)
                                           )
                    elif kwargs["animated"].find("slide") == 0:
                        slide_dir = kwargs["animated"].split("_")[1] if len(kwargs["animated"].split("_")) >= 2 else "random"
                        slide_spec = kwargs["animated"].split("_")[2] if len(kwargs["animated"].split("_")) == 3 else "left"
                        if slide_dir not in ["random", "vertical", "horizontal"]:
                            raise ValueError("Check animation direction for scatter!")
                        if slide_spec not in ["left", "right"]:
                            raise ValueError("Check animation details for scatter!")

                        init_xs, init_ys = None, None
                        W = (lambda x: x[1] - x[0])(self.get_xlim())
                        H = (lambda x: x[1] - x[0])(self.get_ylim())

                        # FIXME: generalize for 3D!
                        if slide_dir == "random":
                            init_xs = (np.random.random(len(args[0])) - 0.5) * W + W / 2
                            init_ys = (np.random.random(len(args[0])) - 0.5) * H + H / 2
                        elif slide_dir == "horizontal":
                            init_ys = np.array(args[1])
                            init_xs = np.array(args[0]) + (slide_spec == "left") * -2 * W + (slide_spec == "right") * 2 * W
                        elif slide_dir == "vertical":
                            init_xs = np.array(args[0])
                            init_ys = np.array(args[1]) + (slide_spec == "left") * -2 * H + (
                                        slide_spec == "right") * 2 * H

                        kwargs = dict_no_animated_key(kwargs)
                        self._actions += [(method_name, [init_xs, init_ys], kwargs)]
                        self.add_animation(SetCoordsAnimation(plt_result_key, np.array(args).T,
                                                              anim_time)
                                           )
                    else:
                        raise ValueError(f"No such animation method for {method_name}!")
                elif method_name == "hist":
                    if kwargs["animated"] == True:
                        kwargs["animated"] = "draw"
                    kwargs = dict_no_animated_key(kwargs)
                    self._actions += [(method_name, [[coord[0]] * len(coord) for coord in args], kwargs)]
                    self.add_animation(DrawLineAnimation(plt_result_key,
                                                         *args,
                                                         anim_time=anim_time)
                                       )
                else:
                    raise NotImplementedError(f"add_plot_action not implemented for method {method_name}!")

                return plt_result_key
            else:
                self._actions += [(method_name, args, dict_no_animated_key(kwargs))]
                return plt_result_key

        self._actions += [(method_name, args, kwargs)]
        return plt_result_key

    def add_animation(self, *anims, anim_time=None):
        assert len(anims) >= 1

        res_anims = []
        biggest_N = 0
        for anim in anims:
            plot_elem_key = anim.mut_obj
            if type(plot_elem_key) != str or "grp" not in plot_elem_key:
                res_anims += [anim]
                biggest_N = max(biggest_N, anim._N)
            else:
                req_anims = anim.animations if anim.__class__.__name__ == "PWNAnimationGroup" else [anim]
                for a in req_anims:
                    biggest_N = max(biggest_N, a._N)
                    for sub_elem_key in self._shared_data["plt_results"][plot_elem_key].subs:
                        a_copy = a.copy()
                        a_copy.mut_obj = sub_elem_key
                        res_anims += [a_copy]

        if anim_time is not None:
            biggest_N = anim_time // _ANIMATION_STEP_TIME
            for anim in res_anims:
                anim._N = biggest_N

        anim_grp = PWNAnimationGroup(self.figure, res_anims,
                                     biggest_N * _ANIMATION_STEP_TIME,
                                     _ANIMATION_STEP_TIME)
        self._actions += [("anim", None, anim_grp)]
        n_prev_anims = len([v for v in self._actions if v[0] == "anim"])
        return f"anim_{n_prev_anims}"

    def sleep(self, sleep_time):
        self.add_animation(Sleep(sleep_time))

    def remove_node(self, node_id, animated=False, anim_time=-1):
        # if node_id not in self._shared_data["plt_results"]:
        #     raise KeyError
        if animated == False:
            animated = "immediately"
        elif animated == True:
            animated = "blur"

        if animated == "blur":
            self.add_animation(SetColorAnimation(node_id, "white", anim_time))
        elif animated == "immediately":
            pass
        else:
            raise ValueError("animated type unsupported!")

        self.add_animation(SetCoordsAnimation(node_id, None, 100))
        # TODO: remove key from shared_data["plt_results"]
        # def remove_key(data):
        #     # new_data = data
        #     del data["plt_results"][node_id]
        #     # return new_data
        #
        # self.add_custom_action(remove_key)

    def set_focus(self, node_id=None, animated=False):
        focus_data_n = max([0] + [int(key.split("_")[1]) for key in self._shared_data["data"] if "focus" in key]) + 1
        self._shared_data["data"][f"focus_{focus_data_n}"] = node_id

        def _setfocus(data):
            first_focus_n = min([int(key.split("_")[1]) for key in self._shared_data["data"] if "focus" in key])
            node_id = data["data"][f"focus_{first_focus_n}"]
            del data["data"][f"focus_{first_focus_n}"]

            all_points = []
            pt_src_ids = [node_id]

            if node_id is None:
                pt_src_ids = [pid
                              for pid in data["plt_results"]
                              if (pid not in ["ax"]) and ("grp" not in pid) and ("patch" not in pid) and ("text" not in pid)]

            for pid in pt_src_ids:
                obj = data["plt_results"][pid]
                if type(obj) == list:
                    obj = obj[0]
                if getattr(obj, "get_xy", None):
                    sub_pts = obj.get_xy()
                elif getattr(obj, "get_center", None):
                    sub_pts = obj.get_center()
                elif getattr(obj, "get_position", None):
                    sub_pts = obj.get_position()
                elif getattr(obj, "get_offsets", None):
                    data0 = np.array(obj.get_offsets())
                    if getattr(obj, "_offsets3d", None):
                        data0 = np.hstack((data0, np.array(obj._offsets3d).reshape((-1, 1))))
                    sub_pts = data0
                    # if len(sub_pts) == 1:
                    #     sub_pts = np.array([[] for c_coord in sub_pts[0]])

                elif getattr(obj, "get_data_3d", None):
                    sub_pts = np.array(obj.get_data_3d()).T
                elif getattr(obj, "get_data", None):
                    sub_pts = np.array(obj.get_data()).T
                else:
                    raise NotImplementedError
                # try:
                all_points += np.array(sub_pts).tolist()
                # except:
                #     raise Exception(str(sub_pts) + "\n\n" + str(type(obj)))

            all_points = np.array(all_points)

            # if flag:
            #     raise Exception(str(all_points))

            limits = np.array([[all_points[:, i].min(),
                                all_points[:, i].max()]
                               for i in range(all_points.shape[1])])
            max_lims = limits[np.argmax(limits[:,1] - limits[:, 0])]
            radius = (max_lims[1] - max_lims[0]) / 2
            radius *= 1.2
            # limits = [] * len(limits)

            pt_center = (all_points.max(axis=0) + all_points.min(axis=0)) / 2  # all_points.mean(axis=0)

            limits = np.array([[c - radius, c + radius] for c in pt_center])

            axes = ["x", "y", "z"]
            if animated == True:
                res_anims = []
                anim_time = _DEFAULT_ANIMATION_TIME
                for i, lim in enumerate(limits):
                    res_anims += [SetAxisLimitsAnimation("ax", axes[i], lim, anim_time)]
                return [("anim", None, PWNAnimationGroup(self.figure, res_anims, anim_time, _ANIMATION_STEP_TIME))]
            else:
                acts = [(f"set_{axes[i]}lim", lim, {}) for i, lim in enumerate(limits)]
                return acts

        self.add_custom_action(_setfocus)

    def to_gif(self):
        raise NotImplementedError
