from manim import *

class Pythagorean_Proof(Scene):
    def construct(self):
        right_angle_vertex = LEFT * 2 + DOWN * 2
        horizontal_vertex = RIGHT * 2 + right_angle_vertex
        vertical_vertex = UP * 2 + right_angle_vertex
        
        vertices = [right_angle_vertex, horizontal_vertex, vertical_vertex]
        right_triangle = Polygon(*vertices)
        right_triangle.set_color(GREEN)
        # right_triangle.shift(RIGHT * 2 + DOWN * 2)

        self.play(Create(right_triangle))
        self.wait(2)
        """
        tilted_square = Square(side_length=2).rotate(PI / 4)  
        tilted_square.set_color(BLUE)
        self.play(Create(tilted_square))

        duplicate_square = tilted_square.copy()  
        duplicate_square.set_color(GREEN)
        duplicate_square.move_to(tilted_square.get_center())
        self.play(Create(duplicate_square))

        self.play(ScaleInPlace(duplicate_square, 1.5))
        self.play(Rotate(duplicate_square, angle = PI / 4))  

        self.wait(2)
        """