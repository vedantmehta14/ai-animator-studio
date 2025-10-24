from manim import *

class GeneratedScene(Scene):
    def construct(self):
        square = Square(color=ORANGE, fill_opacity=1)
        circle = Circle(color=RED, fill_opacity=1)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(circle))