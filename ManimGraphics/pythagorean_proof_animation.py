from manim import *

class Pythagorean_Proof(Scene):
    def construct(self):
        self.labels_dict = {}

        initial_right_triangle = self.create_initial_triangle()
        self.add_initial_triangle_labels(initial_right_triangle)
        
        small_square = self.draw_square_on_hypotenuse(initial_right_triangle)
        self.add_labels_to_square(small_square)
        small_square.set_z_index(1)

        large_square_side_triangles = self.copy_move_rotate_triangles(initial_right_triangle, small_square)
        #self.fit_triangles_into_square(square)

        self.add_labels_to_new_triangles()

        # Shift everything to the left for proof
        shift_amount = LEFT * 3.5  # Adjust this value as needed
        self.play(Group(*self.mobjects).animate.shift(shift_amount))

        self.write_proof_line1()
        self.write_proof_line2_large_square_equation(large_square_side_triangles)
        self.write_proof_line2_small_square_equation(small_square)
        self.write_proof_line2_triangles_equation(self.triangle_copies[0])
        self.write_proof_line3()
        self.write_proof_last_line()

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

        # Add labels to the global dictionary
        self.labels_dict['initial_triangle'] = {'a': label_a, 'b': label_b, 'c': label_c}
        
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

        # Add labels to the global dictionary
        self.labels_dict['square'] = {'c2': label_c2, 'c3': label_c3, 'c4': label_c4}
        
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

        # Extract the first two triangles
        square_side_triangles = self.triangle_copies[:2]
        return square_side_triangles

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

        return label_a, label_b

    def add_labels_to_new_triangles(self):
        label_positions = [
            (UP, LEFT),
            (UP, RIGHT),   
            (DOWN, RIGHT)  
        ]

        for i, triangle in enumerate(self.triangle_copies):
            label_a_pos, label_b_pos = label_positions[i]
            label_a, label_b = self.add_a_b_labels_to_triangle(triangle, label_a_pos, label_b_pos)
            self.labels_dict[f"triangle_{i + 2}"] = {'a': label_a, 'b': label_b}

        self.wait(0.5)

    def midpoint(p1, p2):
        return (p1 + p2) / 2

    def write_proof_line1(self):
        proof_start_text = Tex(r"Large square = small square + 4 edge triangles")
        proof_start_text.scale(0.7)  # Make the text smaller
        proof_start_text.shift(RIGHT * 2.8 + UP * 2)  # Shift the text up a little
        self.play(FadeIn(proof_start_text))
        self.proof_line1 = proof_start_text
        self.wait(0.5)

    def write_proof_line2_large_square_equation(self, largeSquareSide):
        # Get the 90-degree vertex of the first triangle (start of the line)
        start_vertex = largeSquareSide[0].get_vertices()[0]
        # Get the 90-degree vertex of the second triangle (end of the line)
        end_vertex = largeSquareSide[1].get_vertices()[0]
        # Create a line between the two vertices
        large_square_side_highlight = Line(start=start_vertex, end=end_vertex, color=YELLOW, stroke_width = 8)
        large_square_side_highlight.set_z_index(2)
        self.play(FadeIn(large_square_side_highlight))

        # Determine the position of the bottom-left corner of the last line
        text_bottom_left = self.proof_line1.get_corner(DOWN + LEFT)

        partial_text_large_square = Tex(r"${ (a+b)^2 \hspace{20pt} = }$")
        partial_text_large_square.scale(0.7)  # Adjust scale as needed
        partial_text_large_square.move_to(text_bottom_left)
        partial_text_large_square.shift(DOWN * 0.5 + RIGHT * 1.2)
        self.proof_line2_partial_text_large_square = partial_text_large_square
        self.play(FadeIn(partial_text_large_square))

        self.play(FadeOut(large_square_side_highlight))
        self.wait(0.5)

    def write_proof_line2_small_square_equation(self, smallSquare):
        # Get a 90-degree vertex of the square (start of the line)
        start_vertex = smallSquare.get_vertices()[1]
        # Get the next 90-degree vertex of the square (end of the line)
        end_vertex = smallSquare.get_vertices()[2]
        # Create a line between the two vertices
        small_square_side_highlight = Line(start=start_vertex, end=end_vertex, color=YELLOW, stroke_width=8)
        small_square_side_highlight.set_z_index(2)
        self.play(FadeIn(small_square_side_highlight))
        self.wait(0.5)

        partial_text_small_square = Tex(r"${ c^2 \hspace{25pt} + }$")
        partial_text_small_square.scale(0.7)  # Adjust scale as needed
        partial_text_small_square.next_to(self.proof_line2_partial_text_large_square, RIGHT, buff=1)
        self.proof_line2_partial_text_small_square = partial_text_small_square
        self.play(FadeIn(partial_text_small_square))

        self.play(FadeOut(small_square_side_highlight))
        self.wait(0.5)

    def write_proof_line2_triangles_equation(self, triangle):
        # Get a 90-degree vertex of the triangle (start of the line)
        start_vertex_line1 = triangle.get_vertices()[0]
        # Get the next 90-degree vertex of the triangle (end of the line)
        end_vertex_line1 = triangle.get_vertices()[1]
        # Create a line between the two vertices
        triangle_side_highlight_1 = Line(start=start_vertex_line1, end=end_vertex_line1, color=YELLOW, stroke_width=8)
        triangle_side_highlight_1.set_z_index(2)
        self.play(FadeIn(triangle_side_highlight_1))

        # Get a 90-degree vertex of the triangle (start of the line)
        start_vertex_line2 = triangle.get_vertices()[0]
        # Get the next 90-degree vertex of the triangle (end of the line)
        end_vertex_line2 = triangle.get_vertices()[2]
        # Create a line between the two vertices
        triangle_side_highlight_2 = Line(start=start_vertex_line2, end=end_vertex_line2, color=YELLOW, stroke_width=8)
        triangle_side_highlight_2.set_z_index(2)
        self.play(FadeIn(triangle_side_highlight_2))
        self.wait(0.5)

        partial_text_triangle = Tex(r"${ 4 \times (\frac{ab}{2}) }$")
        partial_text_triangle.scale(0.7)  # Adjust scale as needed
        partial_text_triangle.next_to(self.proof_line2_partial_text_small_square, RIGHT, buff=0.5)
        self.proof_line2_partial_text_triangle = partial_text_triangle
        self.play(FadeIn(partial_text_triangle))

        self.play(FadeOut(triangle_side_highlight_1))
        self.play(FadeOut(triangle_side_highlight_2))
        self.wait(0.5)

    def write_proof_line3(self):
        # Determine the position of the bottom-left corner of the last line
        text_bottom_left = self.proof_line2_partial_text_large_square.get_corner(DOWN + LEFT)

        proof_line3_text = Tex(r"${ a^2 + 2ab + b^2 \hspace{20pt} = c^2 \hspace{25pt}+ 2ab }$")
        proof_line3_text.scale(0.7)  # Make the text smaller
        proof_line3_text.move_to(text_bottom_left)
        proof_line3_text.shift(DOWN * 0.5)  # Shift the text up a little
        self.play(FadeIn(proof_line3_text))
        self.proof_line3 = proof_line3_text
        self.wait(0.5)

    def write_proof_last_line(self):
        # Determine the position of the bottom-left corner of the last line
        text_bottom_left = self.proof_line3.get_corner(DOWN + LEFT)

        proof_last_line_text = Tex(r"${ a^2 + b^2 \hspace{20pt} = c^2 \hspace{25pt}}$")
        proof_last_line_text.scale(0.7)  # Make the text smaller
        proof_last_line_text.move_to(text_bottom_left)
        proof_last_line_text.shift(DOWN * 0.5)  # Shift the text up a little
        self.play(FadeIn(proof_last_line_text))
        self.proof_last_line = proof_last_line_text
        self.wait(0.5)