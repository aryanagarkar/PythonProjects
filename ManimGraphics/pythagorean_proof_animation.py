from manim import *

class Pythagorean_Proof(Scene):
    def construct(self):
        right_triangle = self.create_triangle()
        self.add_triangle_labels(right_triangle)
        
        square = self.draw_square_on_hypotenuse(right_triangle)
        self.add_labels_to_square(square)

    def create_triangle(self):
        right_angle_vertex = LEFT * 2 + DOWN * 2
        horizontal_vertex = RIGHT * 2 + right_angle_vertex
        vertical_vertex = UP * 2 + right_angle_vertex
        
        vertices = [right_angle_vertex, horizontal_vertex, vertical_vertex]
        right_triangle = Polygon(*vertices)
        right_triangle.set_color(GREEN)

        self.play(Create(right_triangle))
        self.wait(0.5)
        return right_triangle

    def add_triangle_labels(self, triangle):
        # Calculate midpoints for the sides to position the labels
        vertices = triangle.get_vertices()
        mid_a = (vertices[0] + vertices[1]) / 2  # Midpoint of side a
        mid_b = (vertices[0] + vertices[2]) / 2  # Midpoint of side b
        mid_c = (vertices[1] + vertices[2]) / 2  # Midpoint of side c
        
        # Create labels for the sides
        label_a = MathTex("a").next_to(mid_a, DOWN)
        label_b = MathTex("b").next_to(mid_b, LEFT)
        label_c = MathTex("c").next_to(mid_c, UP)
        
        # Fade in the labels
        self.play(FadeIn(label_a), FadeIn(label_b), FadeIn(label_c))
        self.wait(0.5)

    def draw_square_on_hypotenuse(self, triangle):
        vertices = triangle.get_vertices()
        hypotenuse_start = vertices[1]  
        hypotenuse_end = vertices[2]
        hypotenuse_vector = hypotenuse_end - hypotenuse_start

        unit_vector = hypotenuse_vector / np.linalg.norm(hypotenuse_vector)
        perp_vector = np.array([unit_vector[1], -unit_vector[0], 0])

        vertex_1 = hypotenuse_start
        vertex_2 = hypotenuse_end
        vertex_3 = vertex_2 + perp_vector * np.linalg.norm(hypotenuse_vector)
        vertex_4 = vertex_1 + perp_vector * np.linalg.norm(hypotenuse_vector)

        square = Polygon(vertex_1, vertex_2, vertex_3, vertex_4)
        square.set_color(RED)

        self.play(Create(square))
        self.wait(0.5)
        return square

    def add_labels_to_square(self, square):
        # Calculate midpoints for the sides to position the labels
        vertices = square.get_vertices()
        mid_2_3 = (vertices[1] + vertices[2]) / 2
        mid_3_4 = (vertices[2] + vertices[3]) / 2
        mid_4_1 = (vertices[3] + vertices[0]) / 2
        
        # Create labels for the sides
        label_c2 = MathTex("c").next_to(mid_2_3, RIGHT)
        label_c3 = MathTex("c").next_to(mid_3_4, DOWN)
        label_c4 = MathTex("c").next_to(mid_4_1, LEFT)
        
        # Fade in the labels
        self.play(FadeIn(label_c2), FadeIn(label_c3), FadeIn(label_c4))
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