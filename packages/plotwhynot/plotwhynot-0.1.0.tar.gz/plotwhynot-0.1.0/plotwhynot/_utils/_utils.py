
def dict_no_animated_key(d):
    return {k: v for k,v in d.items() if k not in ["animated", "anim_time"]}


def get_plot_method_key(method_name, key):
    def get_color_key(name):
        if name in ["scatter", "plot"]:
            return "c"
        # if name in ["plot"]:
        #     return "color"
        return "color"

    def get_data_key(name):
        if name in ["plot"]:
            return "get_data"
        raise NotImplementedError

    if key == "color":
        return get_color_key(method_name)
    elif key == "data":
        return get_data_key(method_name)

    raise ValueError("Key unsupported!")
