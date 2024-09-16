from manim import *

class FourierSeries(Scene):
    def construct(self):
        num_terms = 5  # Number of Fourier series terms (circles)
        initial_circle_radius = 1  # Radius of the first circle
        rotation_speeds = [k * PI for k in range(1, num_terms + 1)]  # Frequencies for each term
        colors = [RED, GREEN, BLUE, YELLOW, ORANGE]  # Colors for circles

        # Create the point that will be traced
        point = Dot(color=WHITE)
        
        # Initialize arrays to store the circles, radii, and rotations
        circles = []
        radii = []
        rotations = []

        # Create circles
        circles, radii = self.create_circles(num_terms, initial_circle_radius)  
        last_circle = circles[-1]

        # Animate the creation of circles
        for circle in circles:
            self.play(Create(circle))  # Animate the creation of each circle

        # Add lines to visualize the rotation of each circle
        lines = []
        for circle in circles:
            line = Line(circle.get_center(), circle.get_center() + RIGHT * circle.radius, color=YELLOW)
            self.add(line)
            lines.append(line)

        # The point starts at the edge of the last circle
        point.move_to(last_circle.get_center() + RIGHT * radii[-1])
        self.add(point)

        # Create the path for tracing the point's movement
        path = VMobject(color=WHITE, stroke_width=3)
        path.set_points_as_corners([point.get_center(), point.get_center()])
        self.add(path)

        # Define the updater for the path tracing
        def update_path(mob, dt):
            for i, circle in enumerate(circles):
                # Update the corresponding line
                lines[i].put_start_and_end_on(circle.get_center(), circle.get_center() + RIGHT * circle.radius)

            # Update the point's position and path
            point.move_to(circles[-1].get_right())
            new_point = point.get_center()
            path.add_line_to(new_point)

        # Add updaters for rotation
        for i, circle in enumerate(circles):
            circle.add_updater(lambda c, dt, i=i: c.rotate(rotation_speeds[i] * dt, about_point=c.get_center()))

        # Add updaters for lines
        for line, circle in zip(lines, circles):
            line.add_updater(lambda l, dt, c=circle: l.put_start_and_end_on(c.get_center(), c.get_center() + RIGHT * c.radius))

        # Add the updater to the path
        path.add_updater(update_path)
        self.wait(10)

    def create_circles(self, num_terms, initial_circle_radius):
        circles = []
        radii = []
        current_position = ORIGIN + LEFT * 3
        angle = PI / 4

        for i in range(num_terms):
            radius = initial_circle_radius / (i + 1)
            circle = Circle(radius=radius, color=GREEN)
            circle.move_to(current_position)
            circles.append(circle)
            radii.append(radius)

            if i != num_terms - 1:
                next_radius = initial_circle_radius / (i + 2)
                distance = radius + next_radius

                x_offset = distance * np.cos(angle)
                y_offset = distance * np.sin(angle)

                angle = angle - (10 * DEGREES)
                current_position = current_position + np.array([x_offset, y_offset, 0])

        return circles, radii