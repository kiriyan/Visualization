from manimlib import *
import librosa.display
import numpy as np
from pydub import AudioSegment

# 1秒=1000毫秒
SECOND = 1000
# 音乐文件
AUDIO_PATH = 'music.mp3'
time_end = 170

def split_music(begin, end, filepath):
    # 导入音乐
    song = AudioSegment.from_mp3(filepath)

    # 取begin秒到end秒间的片段
    song = song[begin * SECOND: end * SECOND]

    # 存储为临时文件做备份
    #temp_path = 'backup/' + filepath
    temp_path = filepath
    song.export(temp_path)
    return temp_path

music, sr = librosa.load(split_music(0, time_end+1, AUDIO_PATH))

music = np.array([mic for mic in music if mic > 0])
music_map = []
state_count, pic_state = 2, 141  # 一秒内的频谱状态数，每个状态的音符数
pic_count = state_count * pic_state  # 一秒内的总音符数
for i in range(1, time_end*pic_count+1):
    music_map.append(music[int(i / (time_end*pic_count) * len(music))-1])
    if len(music_map) % pic_state == 0:
        music_map = [
            *music_map[0:len(music_map)-pic_state],
            *list(reversed(sorted(music_map[len(music_map)-pic_state:len(music_map)])))
        ]
#print(len(music_map))
max_z = max(music_map)
"""
Poses = [
            [0], [1, 5, 6], [2, 7, 12, 11, 10],
            [3, 8, 13, 18, 17, 16, 15],
            [4, 9, 14, 19, 24, 23, 22, 21, 20]
        ]
"""
Poses = [
    *[[i] for i in range(pic_state)]
]

def addPoin(x, y):
    # return a Point pos
    return np.array([x, y, 0])


class boxes(Scene):
    def time_pos(self, bh, start, mobject):
        # points_pos srat by the time(start by 0s)
        index = 0  # where the point is in Poses
        time = self.time - start
        k = int(np.floor(time / (1 / state_count)))  # time is between 0.5k and 0.5(k+1)
        # stander_height is now, k_max_height is before
        max_height = 20; min_height = 15
        before_height, now_height = self.k_max_height, self.stander_height
        if bh in Poses[0]:
            index = 0
            if (music_map[pic_state * k] / max_z * (max_height+min_height)/2) > 3:
                self.stander_height = 3
            elif (music_map[pic_state * k] / max_z * (max_height+min_height)/2) < 2:
                self.stander_height = 2
            else:
                self.stander_height = music_map[pic_state * k + index] / max_z * (max_height+min_height)/2
            # before_height, now_height = self.k_max_height, self.stander_height
            """if self.stander_height == self.k_max_height and music_map[pic_state*k] > music_map[pic_state*k-pic_state]:
                now_height += 0.2
            elif self.stander_height == self.k_max_height and music_map[pic_state*k] < music_map[pic_state*k-pic_state]:
                now_height -= 0.2"""
        for i in range(1, pic_state):
            if bh in Poses[i]: index = i
        self.k_max_height = self.stander_height
        # else return False
        before_height *= music_map[pic_state * k - pic_state + index] / music_map[pic_state * k - pic_state]
        now_height *= music_map[pic_state * k + index] / music_map[pic_state * k]
        height = before_height
        height += (time - (1/state_count) * k) / (1/state_count) * (now_height - before_height)
        #print(bh, " : ", height, ";; time = ", time)
        return height

    def updater_fun(self, bh, start, mobject):
        fun = lambda m: m.set_depth(self.time_pos(bh=bh, start=start, mobject=mobject), True)
        return fun

    def aligh_fun(self, mobject):
        fun = lambda n: n.move_to(np.array([mobject.get_center()[0], mobject.get_center()[1], mobject.get_depth()/2]))
        return fun

    def construct(self):
        frame = self.camera.frame
        frame.set_height(40)
        self.Squares = VGroup()
        self.Prisms = VGroup()
        self.k_max_height, self.stander_height = 0, 0  # stander_height is now, k_max_height is before
        # self.embed()
        text = Text("Akie").set_height(18)
        now = None
        for point in text.get_all_points():
            # squre = Square3d(side_length=1).move_to(point)
            if now is not None:
                pd = False
                for mob in self.Squares:
                    # if squre
                    onemob = Square3D(side_length=2).move_to(mob.get_center())
                    if onemob.is_point_touching(point):
                        pd = True
                        break
                if pd: continue
            A = Square3D(side_length=1).move_to(point)
            self.Squares.add(A)
            #self.add(self.Squares[-1])
            now = point
        for squ in self.Squares:
            pri = Prism(dimensions=[1.5, 1.5, 0.1]).move_to(squ.get_center())
            self.Prisms.add(pri)
            self.add(self.Prisms[-1])

        self.start_time = self.time

        for i in range(len(self.Prisms)):
            self.Prisms[i].add_updater(
                # lambda m: m.move_to(self.time_pos(bh=bh, time=self.time-now_time, mobject=m))
                update_function=self.updater_fun(bh=i, start=self.start_time, mobject=self.Prisms[i])
            )
            self.Prisms[i].add_updater(
                update_function=self.aligh_fun(mobject=self.Prisms[i])
            )
        self.Prisms.set_color_by_gradient(RED_D, RED_A, GOLD_C)

        #self.wait(80)
        self.wait(15)
        self.play(
            # 在过渡期间移动相机帧
            frame.increment_phi, 60 * DEGREES,
            frame.increment_theta, -20 * DEGREES,
            run_time=7
        )
        # 添加自动旋转相机帧
        frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        self.wait(147)
        # 最大高度为3




