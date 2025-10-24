from manim import *

class GeneratedScene(Scene):
    def construct(self):
        circle = Circle(color=YELLOW, fill_opacity=1)
        hexagon = RegularPolygon(n=6, color=ORANGE, fill_opacity=1)
        self.play(Create(circle))
        self.play(Transform(circle, hexagon))
        self.play(FadeOut(hexagon))