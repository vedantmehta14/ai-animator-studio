from manim import *

class GeneratedScene(Scene):
    def construct(self):
        circle = Circle(color=RED)
        self.play(Create(circle))
        self.wait(1)