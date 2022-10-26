from manimlib import *

class test(Scene):
    def construct(self):
        frame = self.camera.frame
        inital_square = Square3D(side_length=2).move_to([0,0,0])
        self.add(inital_square)
        self.play(
            # 在过渡期间移动相机帧
            frame.increment_phi, 60 * DEGREES,
            frame.increment_theta, -20 * DEGREES
        )
        a = Prism(dimensions=[1,2,1]).set_color_by_gradient(RED_D, RED_A, GOLD_C)
        a.add_updater(
            lambda m: m.move_to(np.array([m.get_center()[0], m.get_center()[1], m.get_depth()/2]))
        )
        self.play(FadeIn(a), run_time=5)
        a.set_depth(5, True)
        #self.play(a[1].animate.shift(RIGHT*3))
        self.wait(5)

