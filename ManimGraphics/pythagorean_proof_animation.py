from manim import *

class Pythagorean_Proof(Scene):
    def construct(self):
        initial_right_triangle = self.create_initial_triangle()
        self.add_initial_triangle_labels(initial_right_triangle)
        
        square = self.draw_square_on_hypotenuse(initial_right_triangle)
        self.add_labels_to_square(square)
        square.set_z_index(1)

        self.copy_move_rotate_triangles(initial_right_triangle, square)
        #self.fit_triangles_into_square(square)

        self.add_labels_to_new_triangles()

    def create_initial_triangle(self):
        right_angle_vertex = LEFT * 2 + DOWN * 2
        horizontal_vertex = RIGHT * 2 + right_angle_vertex
        vertical_vertex = UP * 2 + right_angle_vertex
        
        vertices = [right_angle_vertex, horizontal_vertex, vertical_vertex]
        right_triangle = Polygon(*vertices)
        right_triangle.set_color(GREEN)

        self.play(Create(right_triangle))
        self.wait(0.5)
        return right_triangle

    def add_initial_triangle_labels(self, triangle):
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
        self.wait(0.5)

    def copy_move_rotate_triangles(self, triangle, square):
        vertices = square.get_vertices()
        triangle_copies = []
        #diagnonal_offset = 0.5

        directions = [UP * 4, RIGHT * 4, DOWN * 4]
        #diagonal_offset_directions = [LEFT * diagnonal_offset, RIGHT * diagnonal_offset, DOWN * diagnonal_offset]
        angle_of_rotation_clockwise = -PI / 2
        
        for i, direction in enumerate(directions):
            if i == 0:
                new_triangle = triangle.copy()
            else:
                new_triangle = triangle_copies[-1].copy()
            
            triangle_copies.append(new_triangle)

            self.play(new_triangle.animate.shift(direction))
            
            rotate_angle = angle_of_rotation_clockwise
            rotate_point = new_triangle.get_vertices()[0]
            self.play(new_triangle.animate.rotate(rotate_angle, about_point=rotate_point))

            #adjust_distance = diagonal_offset_directions[i]
            #self.play(new_triangle.animate.shift(adjust_distance))
        
        self.wait(0.5)
        self.triangle_copies = triangle_copies

    def fit_triangles_into_square(self, square):
        vertices = square.get_vertices()
        for i, triangle in enumerate(self.triangle_copies):
            start, end = vertices[i], vertices[(i + 1) % 4]
            direction_vector = end - start
            self.play(triangle.animate.move_to(start + direction_vector / 2), run_time=1.5)

        self.wait(2)

    def add_a_b_labels_to_triangle(self, triangle, label_a_pos, label_b_pos):
        vertices = triangle.get_vertices()
        mid_a = (vertices[0] + vertices[1]) / 2
        mid_b = (vertices[0] + vertices[2]) / 2

        label_a = MathTex("a").next_to(mid_a, label_a_pos)
        label_b = MathTex("b").next_to(mid_b, label_b_pos)
        self.play(FadeIn(label_a), FadeIn(label_b))

    def add_labels_to_new_triangles(self):
        label_positions = [
            (UP, LEFT),
            (UP, RIGHT),   
            (DOWN, RIGHT)  
        ]

        for i, triangle in enumerate(self.triangle_copies):
            label_a_pos, label_b_pos = label_positions[i]
            self.add_a_b_labels_to_triangle(triangle, label_a_pos, label_b_pos)

        self.wait(0.5)

    def midpoint(p1, p2):
        return (p1 + p2) / 2
