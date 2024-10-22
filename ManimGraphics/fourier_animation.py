from manim import *
import numpy as np

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

        self.n_vectors = 40
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
        
    def get_fourier_vectors(self, path):
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

    def get_tex_symbol(self, symbol, color):
        symbol = Tex(symbol, stroke_width=1, fill_opacity=1, height=4)

        if color is not None:
            symbol.set_color(color)

        return symbol

    def get_path_from_symbol(self, symbol):
        return symbol.family_members_with_points()[0]

    def construct(self):
        # Symbols to draw.
        symbol = self.get_tex_symbol("$\\pi$", RED)

        # Symbol path to trace.
        symbol_path = self.get_path_from_symbol(symbol)

        # Fourier series for symbol1
        vectors = self.get_fourier_vectors(symbol_path)
        circles = self.get_circles(vectors)
        drawn_path = self.get_drawn_path(vectors).set_color(RED)

        # Camera updater
        last_vector = vectors[-1]

        # Scene start
        self.wait(1)
        
        # Create a list for arrow animations
        arrow_animations = []
        for arrow in vectors:
            arrow_animations.append(GrowArrow(arrow))

        # Create a list for circle animations
        circle_animations = []
        for circle in circles:
            circle_animations.append(Create(circle))

        # Execute all create animations.
        self.play(
            *arrow_animations,
            *circle_animations,
            run_time=2.5,
        )

        # Add objects to scene
        self.add( 
            vectors,
            circles,
            drawn_path.set_stroke(width = self.drawn_path_stroke_width)
        )
 
        # Add updaters and start vector clock
        vectors.add_updater(self.update_vectors)
        circles.add_updater(self.update_circles)
        drawn_path.add_updater(self.update_path)
        self.toggle_vector_clock(start=True)

        self.play(self.slow_factor_tracker.animate.set_value(0.5), run_time = self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.5 * self.cycle_seconds)
        
        # Remove updaters so can animate.
        self.toggle_vector_clock(start=False)
        drawn_path.clear_updaters()
        vectors.clear_updaters()
        circles.clear_updaters()

        # Create a single list that contains all the VMobjects to be uncreated
        uncreate_animations = []

        # Add uncreate animations for all objects in vectors
        for arrow in vectors:
            uncreate_animations.append(Uncreate(arrow))

        # Add uncreate animations for all objects in circles
        for circle in circles:
            uncreate_animations.append(Uncreate(circle))

        # Execute all uncreate animations.
        self.play(
            *uncreate_animations,
            run_time=2.5,
        )

        self.wait(3)