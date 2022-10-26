"""
# for the rest of the programme - 3Dtest

def time_pos(bh, time){
    # points_pos change by the time(start by 0s)
    index = 0  # where the point is in Poses
    if bh in Poses[0]: index = 0
    elif bh in Poses[1]: index = 1
    elif bh in Poses[2]: index = 2
    elif bh in Poses[3]: index = 3
    elif bh in Poses[4]: index = 4
    # else return False
    k = int(np.floor(time / 0.5))
    height = music_map[5*k - 5 + index]
    height += (time-0.5*k)/0.5 * (music_map[5*k+index]-music_map[5*k-5+index])
    x, y = Squares[bh].get_center()[0], Squares[bh].get_center()[1]
    return np.array([x, y, height])
}

# updaters
now_time = self.time

Sqaures[i].add_updater(
    lambda m: m.move_to(time_pos(i, self.time - now_time))
) for i in range(len(Sqaures))
"""
import numpy as np

"""
a = [5, 2, 9, 2, 5, 3, 6, 7, 4]
a[3:6].sort()

a = [*a[0:3], *list(reversed(sorted(a[3:6]))), *a[6:len(a)]]
print(a)

Poses = [
            [0], [1, 5, 6], [2, 7, 12, 11, 10],
            [3, 8, 13, 18, 17, 16, 15],
            [4, 9, 14, 19, 24, 23, 22, 21, 20]
        ]

import numpy as np
bhs = np.random.randint(0, 25, 10)
for bh in bhs:
    index = None
    if bh in Poses[0]:
        index = 0
    elif bh in Poses[1]:
        index = 1
    elif bh in Poses[2]:
        index = 2
    elif bh in Poses[3]:
        index = 3
    elif bh in Poses[4]:
        index = 4
    print(bh, " is in Poses: ", index)
"""


from manimlib import *

class test_moving_updaters(Scene):
    def construct(self):
        point = Dot(color=RED).move_to(ORIGIN)
        now = self.time
        self.add(point)
        point.add_updater(
            lambda m: m.shift((0.4*(self.time-now)-m.get_center()[1])*UP)
        )
        #self.play(point.animate.move_to(np.array([4, -10, 0])), run_time=10)
        self.wait(10)


class test_get_points(Scene):
    def construct(self):
        frame = self.camera.frame
        frame.set_height(40)
        text = Text("6").set_height(18)
        points = []
        now = None
        for point in text.get_all_points():
            # squre = Square3d(side_length=1).move_to(point)
            if now is not None:
                pd = False
                for mob in points:
                    # if squre
                    onemob = Square3D(side_length=2).move_to(mob.get_center())
                    if onemob.is_point_touching(point):
                        pd = True; break
                if pd: continue
            A = Square3D(side_length=1).move_to(point)
            points.append(A)
            self.add(points[-1])
            now = point
        print(len(points))

pic_state = 3
Poses = [
    *[[i] for i in range(pic_state)]
]
print(Poses)