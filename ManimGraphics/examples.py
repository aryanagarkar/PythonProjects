from manim import *

class PointMovingOnShapes(Scene):
    def construct(self):
        square = Square(side_length=2)
        square2 = Square(side_length=2)
        rectangle_height = 0.5
        rectangle = Rectangle(height=rectangle_height, width=2)

        # square.set_fill(RED, opacity=1) 
        square.set_stroke(BLUE, width=2)
        square2.set_stroke(BLUE, width=2)
        rectangle.set_stroke(GREEN, width=2)

        square.shift(4 * LEFT + 2 * DOWN)
        square2.shift(4 * RIGHT + 2 * DOWN)
        rectangle.shift(3.5 * LEFT + 2.3 * DOWN)
        
        self.add(square)
        self.play(GrowFromCenter(square))
        self.add(square2)
        self.play(GrowFromCenter(square2))

        self.add(rectangle)
        self.play(Create(rectangle))

        right_center = rectangle.get_right() + 0.04 * DOWN
        left_center = square2.get_left() + 0.35 * DOWN

        dot_wait_time = 0.5  # Time to wait before creating the next dot.
        dot_move_time = 1.0  # Time taken for the dot to move to the right.

        # Create dots at intervals
        dots = []  # List to hold the dots.

        for i in range(100):
            dot = Dot(point=right_center, color=RED)
            dot2 = dot.copy().shift(RIGHT * 5.5)
            self.add(dot)
            self.play(Create(dot))
            dots.append(dot)

            self.play(Transform(dot, dot2), run_time=dot_move_time)
            self.wait(0.1)
            self.play(FadeOut(dot), run_time=0.01)

            # While the first dot is moving, create another dot.
            if i < 4:  # Prevent creating an extra dot after the last one.
                #self.wait(dot_wait_time)  # Wait for specified time for the next dot.
                next_dot = Dot(point=right_center, color=RED)  # Create the next dot.
                self.play(Create(next_dot))  # Create the next dot.
                dots.append(next_dot)  # Store the next dot.

        #dot2 = dot.copy().shift(RIGHT)

        """
        self.add(dot)

        line = Line([3, 0, 0], [5, 0, 0])
        self.add(line)

        self.play(GrowFromCenter(square))
        self.play(Transform(dot, dot2))
        self.play(MoveAlongPath(dot, square), run_time=2, rate_func=linear)
        self.play(Rotating(dot, about_point=[2, 0, 0]), run_time=1.5)
        self.wait()
        """