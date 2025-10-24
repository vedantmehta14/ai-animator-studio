from manim import *

class GeneratedScene(Scene):
    def construct(self):
        square = Square(color=BLUE)
        circle = Circle(color=RED)
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(circle))