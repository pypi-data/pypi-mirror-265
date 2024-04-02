from ._animation import PWNAnimation, np


class ScaleAnimation(PWNAnimation):
    # TODO: reformat code to kwargs with features
    def __init__(self, mut_obj, anim_time=-1, **feature_vals):
        self.mut_features = list(feature_vals.keys())
        if type(mut_obj) != str:
            data0 = self._get_data0(mut_obj)
            self._setup_method(mut_obj)
        else:
            data0 = []
        super().__init__(mut_obj,
                         data0,
                         np.array(list(feature_vals.values())),
                         anim_time)
        self.scale_method = None

    def animate_step(self):
        if self._progress >= self._N - 1:
            self.scale_method(self._data1)
            return  # self._data1
        if len(self._data0) == 0:
            self._data0 = np.array(self._get_data0(self.mut_obj))
        if self.scale_method is None:
            self._setup_method(self.mut_obj)

        new_dims = self._get_prog_data()
        self.scale_method(new_dims)
        self._progress += 1

    def _get_data0(self, obj):
        loc_data0 = []
        for feature in self.mut_features:
            method = getattr(obj, "get_" + feature, None)
            if not method:
                raise ValueError(f"Feature {feature} not found at class {obj.__class__}!")
            loc_data0 += [method()]
            if type(loc_data0[-1]) == list:
                loc_data0[-1] = loc_data0[-1][0]
        return np.array(loc_data0)

        # if getattr(obj, "get_width", None):
        #     w = obj.get_width()
        #     h = obj.get_height()
        # elif getattr(obj, "get_sizes", None):
        #     w = obj.get_sizes()[0]
        # elif getattr(obj, "get_linewidth", None):
        #     w = obj.get_linewidth()
        # else:
        #     # print(obj)
        #     raise Exception("Not implemented for class" + str(obj.__class__))
        # return np.array([w, h])

    def _setup_method(self, obj):
        methods = []
        for feature in self.mut_features:
            method = getattr(obj, "set_" + feature, None)
            if not method:
                raise ValueError(f"Feature {feature} not found at class {obj.__class__}!")
            methods += [method]

        def tmp(cs):
            for i, meth in enumerate(cs):
                val = cs[i]
                if self.mut_features[i] == "sizes":
                    val = [val]
                methods[i](val)

        self.scale_method = lambda c: tmp(c)

        # if getattr(obj, "set_width", None):
        #     def tmp(cs):
        #         obj.set_width(cs[0])
        #         obj.set_height(cs[1])
        #
        #     self.scale_method = lambda c: tmp(c)
        # elif getattr(obj, "set_sizes", None):
        #     self.scale_method = lambda c: obj.set_sizes([c[0]])
        # elif getattr(obj, "set_linewidth", None):
        #     self.scale_method = lambda c: obj.set_linewidth(c[0])
        # else:
        #     raise Exception("Not implemented for class" + str(obj.__class__))
