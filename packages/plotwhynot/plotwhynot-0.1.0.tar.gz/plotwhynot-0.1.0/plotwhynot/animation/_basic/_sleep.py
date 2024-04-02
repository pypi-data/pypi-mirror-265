from ._animation import PWNAnimation


class Sleep(PWNAnimation):
    def __init__(self, anim_time=-1):
        PWNAnimation.__init__(self, None, None, None, anim_time)

    def animate_step(self):
        return

    def _get_data0(self, obj):
        return
