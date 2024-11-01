from manim import *
import numpy as np

from manim import config
config.tex_template.compiler = "xelatex"

class FourierSceneAbstract(ZoomedScene):
    def __init__(self):
        super().__init__()

        self.fourier_symbol_config = {
            "stroke_width": 1,
            "height": 4
        }

        self.vector_config = {
            "tip_length": 0.15,
            "stroke_width": 1.5
        }

        self.circle_config = {
            "stroke_width": 1,
            "color": WHITE
        }

        self.n_vectors = 60   
        self.cycle_seconds = 5
        self.parametric_func_step = 0.001   
        self.drawn_path_stroke_width = 8
        self.path_n_samples = 1000    
        self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1, 1))
        self.freqs.sort(key=abs)

    def setup(self):
        super().setup()
        self.vector_clock = ValueTracker()
        self.slow_factor_tracker = ValueTracker(0)
        self.add(self.vector_clock)

    def toggle_vector_clock(self, start):           
        if start:
            self.vector_clock.add_updater(
                lambda t, dt: t.increment_value(dt * self.slow_factor_tracker.get_value() / self.cycle_seconds)
            )
        else:
            self.vector_clock.clear_updaters()

    def reset_state(self):
        # Stop the vector clock and reset its value
        self.toggle_vector_clock(start=False)
        self.vector_clock.set_value(0)

        # Reset slow factor tracker
        self.slow_factor_tracker.set_value(0)

        # Clear updaters from any other objects
        for obj in self.mobjects:
            obj.clear_updaters()

        # Optionally reset any other class attributes that might have changed
        self.n_vectors = 60
        self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1))
        self.freqs.sort(key=abs)


    def get_fourier_coefs(self, path):
        dt = 1 / self.path_n_samples
        t_range = np.linspace(0, 1, self.path_n_samples)

        points = np.array([path.point_from_proportion(t) for t in t_range])
        complex_points = points[:, 0] + 1j * points[:, 1]

        exponentials = np.exp(-TAU * 1j * np.outer(self.freqs, t_range))
        coefficients = np.dot(exponentials, complex_points) * dt

        return coefficients
        
    def get_fourier_vectors(self, path, num_vectors=None):
        if num_vectors is not None:
            self.n_vectors = num_vectors  
            self.freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1))
            self.freqs.sort(key=abs)
        
        coefficients = self.get_fourier_coefs(path)
        
        vectors = VGroup()
        last_v = None
        for i in range(len(coefficients)):
            coef = coefficients[i]
            freq = self.freqs[i]
            v = Vector([np.real(coef), np.imag(coef)], **self.vector_config)
            
            if last_v:
                v.center_func = last_v.get_end
            else:
                v.center_func = VectorizedPoint(ORIGIN).get_location

            v.freq = freq
            v.coef = coef
            v.phase = np.angle(coef)
            v.shift(v.center_func() - v.get_start())
            v.set_angle(v.phase)
            vectors.add(v)
            last_v = v

        return vectors
        
    def update_vectors(self, vectors):
        for v in vectors:
            time = self.vector_clock.get_value()
            v.shift(v.center_func()-v.get_start())
            v.set_angle(v.phase + time * v.freq * TAU)  
              
    def get_circles(self, vectors):
        circles = VGroup()
        for v in vectors:
            c = Circle(radius = v.get_length(), **self.circle_config)
            c.center_func = v.get_start
            c.move_to(c.center_func())
            circles.add(c)
        return circles

    def update_circles(self, circles):
        for c in circles:
            c.move_to(c.center_func())
            
    def get_drawn_path(self, vectors):    

        def fourier_series_func(t):
            # Initialize the sum as a complex number
            fss = 0 + 0j  # Starting with a complex zero
        
            # Loop through each vector and compute its contribution
            for v in vectors:
                fss += v.coef * np.exp(TAU * 1j * v.freq * t)
        
            # Extract real and imaginary parts
            real_fss = np.array([np.real(fss), np.imag(fss), 0])
            return real_fss
        
        t_range = np.array([0, 1, self.parametric_func_step * 2])
        vector_sum_path = ParametricFunction(fourier_series_func, t_range = t_range)
        broken_path = CurvesAsSubmobjects(vector_sum_path)
        broken_path.stroke_width = 0
        return broken_path

    def update_path(self, broken_path):
        alpha = self.vector_clock.get_value()
        n_curves = len(broken_path)

        # Iterate using a traditional for loop
        for i in range(n_curves):
            subpath = broken_path[i]
            a = i / (n_curves - 1)  # Calculate the corresponding value of a
            if (alpha > a):
                width = self.drawn_path_stroke_width
            else:
                width = 0
            
            subpath.set_stroke(width=width)  # Update the stroke width of the subpath

class OmFourierTransform(FourierSceneAbstract):
    def __init__(self):
        super().__init__()

    def get_path_from_image(self, image):
        return image.family_members_with_points()[0]

    def construct(self):
        image1 = SVGMobject("om_symbol.svg", height=4)
        image2 = SVGMobject("chandrabindu_curve.svg", height=1)
        image3 = SVGMobject("chandrabindu_circle.svg", height=0.5)
        
        image2.shift(2.3*UP+0.9*RIGHT)
        image3.shift(2.9*UP+0.8*RIGHT)

        image1_path = self.get_path_from_image(image1)
        image2_path = self.get_path_from_image(image2)
        image3_path = self.get_path_from_image(image3)

        vectors1 = self.get_fourier_vectors(image1_path, num_vectors=60)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1).set_color(RED)

        vectors2 = self.get_fourier_vectors(image2_path, num_vectors=20)
        circles2 = self.get_circles(vectors2)
        drawn_path2 = self.get_drawn_path(vectors2).set_color(YELLOW)

        vectors3 = self.get_fourier_vectors(image3_path, num_vectors=2)
        circles3 = self.get_circles(vectors3)
        drawn_path3 = self.get_drawn_path(vectors3).set_color(YELLOW)

        self.wait(1)

        arrow_animations1 = [GrowArrow(arrow1) for arrow1 in vectors1]
        circle_animations1 = [Create(circle1) for circle1 in circles1]
        arrow_animations2 = [GrowArrow(arrow2) for arrow2 in vectors2]
        circle_animations2 = [Create(circle2) for circle2 in circles2]
        arrow_animations3 = [GrowArrow(arrow3) for arrow3 in vectors3]
        circle_animations3 = [Create(circle3) for circle3 in circles3]

        self.play(
            *arrow_animations1,
            *circle_animations1,
            *arrow_animations2,
            *circle_animations2,
            *arrow_animations3,
            *circle_animations3,
            run_time=2.5,
        )

        self.add(
            vectors1, 
            circles1,
            drawn_path1.set_stroke(width=self.drawn_path_stroke_width),
            vectors2, 
            circles2,
            drawn_path2.set_stroke(width=self.drawn_path_stroke_width),
            vectors3, 
            circles3,
            drawn_path3.set_stroke(width=self.drawn_path_stroke_width),
        )

        vectors1.add_updater(self.update_vectors)
        circles1.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)

        vectors2.add_updater(self.update_vectors)
        circles2.add_updater(self.update_circles)
        drawn_path2.add_updater(self.update_path)

        vectors3.add_updater(self.update_vectors)
        circles3.add_updater(self.update_circles)
        drawn_path3.add_updater(self.update_path)

        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(0.5), run_time=self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        self.toggle_vector_clock(start=False)

        drawn_path1.clear_updaters()
        vectors1.clear_updaters()
        circles1.clear_updaters()

        drawn_path2.clear_updaters()
        vectors2.clear_updaters()
        circles2.clear_updaters()

        drawn_path3.clear_updaters()
        vectors3.clear_updaters()
        circles3.clear_updaters()

        uncreate_animations = []

        for arrow1 in vectors1:
            uncreate_animations.append(Uncreate(arrow1))

        for circle1 in circles1:
            uncreate_animations.append(Uncreate(circle1))

        for arrow2 in vectors2:
            uncreate_animations.append(Uncreate(arrow2))

        for circle2 in circles2:
            uncreate_animations.append(Uncreate(circle2))

        for arrow3 in vectors3:
            uncreate_animations.append(Uncreate(arrow3))

        for circle3 in circles3:
            uncreate_animations.append(Uncreate(circle3))

        self.play(
            *uncreate_animations,
            run_time=2.5,
        )

        self.wait(3)

class SwastikaFourierTransform(FourierSceneAbstract):
    def __init__(self):
        super().__init__()

    def get_path_from_image(self, image):
        return image.family_members_with_points()[0]

    def construct(self):
        INDIAN_FLAG_SAFFRON = "#FF671F"
        RED = "#C00000"
        YELLOW = "#FFFF33"
        DARK_PINK = "##A9242B"
        PINK = "#EB6170"
        DUSTY_PINK = "#E393A5"


        # Create the first circle
        circle1 = Circle(radius=4)
        circle1.set_stroke(width=0)  
        circle1.set_fill(DARK_PINK, opacity=0)       

        # Create the second circle
        circle2 = Circle(radius=3.5)
        circle2.set_stroke(width=0)  
        circle2.set_fill(DUSTY_PINK, opacity=0)    

        # Add both circles to the scene
        self.add(circle1, circle2)

        # Animate the creation of both circles' outlines
        self.play(Create(circle1), Create(circle2))

        # Animate the fill for each circle, one after the other
        self.play(
            circle1.animate.set_fill(opacity=1),  # Fill the first circle
            run_time=2
        )
        self.play(
            circle2.animate.set_fill(opacity=1),  # Fill the second, larger circle
            run_time=2
        )

        self.wait(2)

        image1 = SVGMobject("swastika.svg", height=6)
        image1.set_stroke(color=YELLOW, width=8)
        
        image1_path = self.get_path_from_image(image1)

        vectors1 = self.get_fourier_vectors(image1_path, num_vectors=190)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1).set_color(YELLOW)

        self.wait(1)

        arrow_animations1 = [GrowArrow(arrow1) for arrow1 in vectors1]
        circle_animations1 = [Create(circle1) for circle1 in circles1]

        self.play(
            *arrow_animations1,
            *circle_animations1,
            run_time=2.5,
        )

        self.wait(0.1)

        self.add(
            vectors1, 
            circles1,
            drawn_path1.set_stroke(width=self.drawn_path_stroke_width),
        )

        vectors1.add_updater(self.update_vectors)
        circles1.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)

        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(1.3), run_time=self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        self.toggle_vector_clock(start=False)

        drawn_path1.clear_updaters()
        vectors1.clear_updaters()
        circles1.clear_updaters()

        uncreate_animations1 = []

        for arrow1 in vectors1:
            uncreate_animations1.append(Uncreate(arrow1))

        for circle1 in circles1:
            uncreate_animations1.append(Uncreate(circle1))

        self.play(
            *uncreate_animations1,
            run_time=2.5,
        )

        self.wait(0.5)

        # Initially set the fill opacity to 0 to make it invisible
        image1.set_fill(color=INDIAN_FLAG_SAFFRON, opacity=0)

        self.add(image1)

        # Fade in the filled shape over a specified duration
        self.play(
            image1.animate.set_fill(opacity=1),  # Animate opacity from 0 to 1
            run_time=3  # Adjust run_time for the desired speed of the fade
        )

        self.wait(1)

        self.reset_state()


        image2 = SVGMobject("swastikaDot.svg", height=0.5)
        image2.set_stroke(width=3)

        image2.shift(UP+RIGHT)

        image2_path = self.get_path_from_image(image2)

        vectors2 = self.get_fourier_vectors(image2_path, num_vectors=2)
        circles2 = self.get_circles(vectors2)
        drawn_path2 = self.get_drawn_path(vectors2).set_color(INDIAN_FLAG_SAFFRON)

        arrow_animations2 = [GrowArrow(arrow2) for arrow2 in vectors2]
        circle_animations2 = [Create(circle2) for circle2 in circles2]

        self.play(
            *arrow_animations2,
            *circle_animations2,
            run_time=2.5,
        )

        self.add(
            vectors2, 
            circles2,
            drawn_path2.set_stroke(width=self.drawn_path_stroke_width),
        )

        vectors2.add_updater(self.update_vectors)
        circles2.add_updater(self.update_circles)
        drawn_path2.add_updater(self.update_path)
 
        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(1.5), run_time=self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        self.toggle_vector_clock(start=False)

        drawn_path2.clear_updaters()
        vectors2.clear_updaters()
        circles2.clear_updaters()

        uncreate_animations2 = []

        for arrow2 in vectors2:
            uncreate_animations2.append(Uncreate(arrow2))

        for circle2 in circles2:
            uncreate_animations2.append(Uncreate(circle2))

        self.play(
            *uncreate_animations2,
            run_time=2.5,
        )

        self.wait(0.5) 

        # Initially set the fill opacity to 0 to make it invisible
        image2.set_fill(color=RED, opacity=0)
        self.add(image2)

        # Fade in the filled shape over a specified duration
        self.play(
            image2.animate.set_fill(opacity=1),  # Animate opacity from 0 to 1
            run_time=3  # Adjust run_time for the desired speed of the fade
        )

        self.wait(1)

        self.reset_state()


        image3 = SVGMobject("swastikaDot.svg", height=0.5)
        image3.set_stroke(width=3)

        image3.shift(UP+LEFT)

        image3_path = self.get_path_from_image(image3)

        vectors3 = self.get_fourier_vectors(image3_path, num_vectors=2)
        circles3 = self.get_circles(vectors3)
        drawn_path3 = self.get_drawn_path(vectors3).set_color(INDIAN_FLAG_SAFFRON)

        arrow_animations3 = [GrowArrow(arrow3) for arrow3 in vectors3]
        circle_animations3 = [Create(circle3) for circle3 in circles3]

        self.play(
            *arrow_animations3,
            *circle_animations3,
            run_time=2.5,
        )

        self.add(
            vectors3, 
            circles3,
            drawn_path3.set_stroke(width=self.drawn_path_stroke_width),
        )

        vectors3.add_updater(self.update_vectors)
        circles3.add_updater(self.update_circles)
        drawn_path3.add_updater(self.update_path)
 
        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(1.5), run_time=self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        self.toggle_vector_clock(start=False)

        drawn_path3.clear_updaters()
        vectors3.clear_updaters()
        circles3.clear_updaters()

        uncreate_animations3 = []

        for arrow3 in vectors3:
            uncreate_animations3.append(Uncreate(arrow3))

        for circle3 in circles3:
            uncreate_animations3.append(Uncreate(circle3))

        self.play(
            *uncreate_animations3,
            run_time=2.5,
        )

        self.wait(0.5)

        # Initially set the fill opacity to 0 to make it invisible
        image3.set_fill(color=RED, opacity=0)
        self.add(image3)

        # Fade in the filled shape over a specified duration
        self.play(
            image3.animate.set_fill(opacity=1),  # Animate opacity from 0 to 1
            run_time=3  # Adjust run_time for the desired speed of the fade
        )

        self.wait(1)

        self.reset_state()


        image4 = SVGMobject("swastikaDot.svg", height=0.5)
        image4.set_stroke(width=3)

        image4.shift(DOWN+RIGHT)

        image4_path = self.get_path_from_image(image4)

        vectors4 = self.get_fourier_vectors(image4_path, num_vectors=2)
        circles4 = self.get_circles(vectors4)
        drawn_path4 = self.get_drawn_path(vectors4).set_color(INDIAN_FLAG_SAFFRON)

        arrow_animations4 = [GrowArrow(arrow4) for arrow4 in vectors4]
        circle_animations4 = [Create(circle4) for circle4 in circles4]

        self.play(
            *arrow_animations4,
            *circle_animations4,
            run_time=2.5,
        )

        self.add(
            vectors4, 
            circles4,
            drawn_path4.set_stroke(width=self.drawn_path_stroke_width),
        )

        vectors4.add_updater(self.update_vectors)
        circles4.add_updater(self.update_circles)
        drawn_path4.add_updater(self.update_path)
 
        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(1.5), run_time=self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        self.toggle_vector_clock(start=False)

        drawn_path4.clear_updaters()
        vectors4.clear_updaters()
        circles4.clear_updaters()

        uncreate_animations4 = []

        for arrow4 in vectors4:
            uncreate_animations4.append(Uncreate(arrow4))

        for circle4 in circles4:
            uncreate_animations4.append(Uncreate(circle4))

        self.play(
            *uncreate_animations4,
            run_time=2.5,
        )

        self.wait(0.5)

        # Initially set the fill opacity to 0 to make it invisible
        image4.set_fill(color=RED, opacity=0)
        self.add(image4)

        # Fade in the filled shape over a specified duration
        self.play(
            image4.animate.set_fill(opacity=1),  # Animate opacity from 0 to 1
            run_time=3  # Adjust run_time for the desired speed of the fade
        )

        self.wait(1)
        
        self.reset_state()


        image5 = SVGMobject("swastikaDot.svg", height=0.5)
        image5.set_stroke(width=3)

        image5.shift(DOWN+LEFT)

        image5_path = self.get_path_from_image(image5)

        vectors5 = self.get_fourier_vectors(image5_path, num_vectors=2)
        circles5 = self.get_circles(vectors5)
        drawn_path5 = self.get_drawn_path(vectors5).set_color(INDIAN_FLAG_SAFFRON)

        arrow_animations5 = [GrowArrow(arrow5) for arrow5 in vectors5]
        circle_animations5 = [Create(circle5) for circle5 in circles5]

        self.play(
            *arrow_animations5,
            *circle_animations5,
            run_time=2.5,
        )

        self.add(
            vectors5, 
            circles5,
            drawn_path5.set_stroke(width=self.drawn_path_stroke_width),
        )

        vectors5.add_updater(self.update_vectors)
        circles5.add_updater(self.update_circles)
        drawn_path5.add_updater(self.update_path)
 
        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(1.5), run_time=self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time=0.5 * self.cycle_seconds)

        self.toggle_vector_clock(start=False)

        drawn_path5.clear_updaters()
        vectors5.clear_updaters()
        circles5.clear_updaters()

        uncreate_animations5 = []

        for arrow5 in vectors5:
            uncreate_animations5.append(Uncreate(arrow5))

        for circle5 in circles5:
            uncreate_animations5.append(Uncreate(circle5))

        self.play(
            *uncreate_animations5,
            run_time=2.5,
        )

        self.wait(0.5)

        image5.set_stroke(width=0)

        # Initially set the fill opacity to 0 to make it invisible
        image5.set_fill(color=RED, opacity=0)

        self.add(image5)

        # Fade in the filled shape over a specified duration
        self.play(
            image5.animate.set_fill(opacity=1),  # Animate opacity from 0 to 1
            run_time=3  # Adjust run_time for the desired speed of the fade
        )

        self.wait(3)