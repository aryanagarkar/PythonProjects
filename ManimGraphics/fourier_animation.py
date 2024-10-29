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
        self.drawn_path_stroke_width = 5
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

class FourierTransform(FourierSceneAbstract):
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