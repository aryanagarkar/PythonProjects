from manim import *

class SquareFunction(Scene):
	def construct(self):
		axes = Axes(
            x_range = [-5, 5.1, 1],
            y_range = [-1.5, 1.5, 1],
            x_length = 2*TAU,
            axis_config = {"color": GREEN},
            tips = True,
            )

		def squareWave(x):
			if int(x)%2 == 0:
				return 1*x//abs(x)
			else:
				return -1*x//abs(x)

		def Sinn(x, n):
			result = 0
			for i in range(1, n+1, 2):
				result += (2/(i*np.pi))*(2)*np.sin(i*x*np.pi)
			return result

		def SINN(x, i):
			return (2/(i*np.pi))*(2)*np.sin(i*x*np.pi)

		square_graph = axes.plot(squareWave, x_range = (-4.9, 4.9, 0.01), **{"discontinuities": [x for x in range(-5, 6)]})
		values = []
		values1 = []
		
		cumulative_terms = ["sin(x)"]
		cumulative_text = Text(" + ".join(cumulative_terms), font_size=24).next_to(axes, UP, buff=0.2)

		index = 1

		for i in range(1, 31, 2):
			values.append(axes.plot(lambda x: SINN(x, i), x_range = (-4.9, 4.9, 0.1)))
			values1.append(axes.plot(lambda x: Sinn(x, i), x_range = (-4.9, 4.9, 0.1), color = BLUE))

		self.add(axes, square_graph,  values[0])
		self.play(ReplacementTransform(values[0], values1[0]))
		self.add(cumulative_text)

		fixed_y_position_for_text = 2
		
		for i in range(1, 15):
			self.play(Create(values[i]))
			self.wait(1)
			self.play(ReplacementTransform(values[i], values1[i]), ReplacementTransform(values1[i - 1], values1[i]))
			
			if i > 1:
				new_term = f"sin({i * 2 - 1}x)"
				cumulative_terms.append(new_term)

			updated_cumulative_text = Text(" + ".join(cumulative_terms), font_size=24).next_to(axes, UP, buff=0)
			self.play(Transform(cumulative_text, updated_cumulative_text))
			cumulative_text = updated_cumulative_text