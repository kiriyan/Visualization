from manimlib import *
import numpy as np
import os

path = "E:\\mathroom\\music-visualization\\album_pictures"
start_year, now_year = 2016, 2022
picture_list = []

def sort_files(path):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 循环判断每个元素是否是文件夹还是文件，是文件夹的话，递归
    outfile = open("content.txt", "w")
    for year in range(start_year, now_year+1):
        for month in range(1, 13):
            for day in range(1, 32):
                file_date = "".join([str(year), ".", str(month), ".", str(day).zfill(2)])
                for file in file_list:
                    tar_file = file.split("-", maxsplit=2)
                    tar_date = "".join(tar_file[0])
                    if tar_date == file_date:
                        picture_list.append([tar_date, "".join(tar_file[1])])
                        print(file, file=outfile)
    outfile.close()


def picture_mob(image_mob):
    pic = SVGMobject("film.svg").set_height(image_mob.get_height(), True)
    pic.set_color(BLACK)
    pic.set_width(image_mob.get_width(), True)
    pic.move_to(image_mob.get_center())
    f_always(pic.move_to, image_mob.get_center)
    return pic


picture_dir = open("content.txt", "r")
picture_group = []; film_group = []; info = []
for line in picture_dir:
    name = line.split("j", maxsplit=2)[0]
    date = Text(name[0:-1].split("-", maxsplit=2)[0], font_size=30, font="SimHei")
    title = Text(name[0:-1].split("-", maxsplit=2)[1], font_size=30, font="SimHei")
    img = ImageMobject(
        filename="".join([path, "\\", line])[0:-5],
        height=5
    ).move_to(np.array([0, 0, 0]))
    picture_group.append(img)
    always(title.next_to, picture_group[-1], UP)
    always(date.next_to, picture_group[-1], DOWN)
    info.append(VGroup(title, date))
    film_group.append(picture_mob(img))

Poses = [np.array([0, 0, 0]), np.array([-5, 0, -10]), np.array([5, 0, -10])]
class pictures(Scene):
    def construct(self):
        frame = self.camera.frame
        self.wait(2)
        for i in range(len(picture_group)):
            if i == 0:
                picture_group[i].move_to(np.array([6*i, 0, 0]))
            elif i > 0:
                picture_group[i].move_to([
                    picture_group[i - 1].get_boundary_point(RIGHT)[0] + picture_group[i].get_width() / 2,
                    0, 0
                ])
            self.play(FadeIn(picture_group[i]), FadeIn(film_group[i]), FadeIn(info[i]), run_time=2)
            if i == 0:
                st_time = self.time
                frame.add_updater(
                    lambda m: m.move_to(np.array([(self.time - st_time), 0, 0]))
                )
            self.wait(3)
        self.wait(10)



