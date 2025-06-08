from manim import *
import sympy as sp

class GeneralFunctionPlot(Scene):
    def __init__(self, equation, x_range=(-5, 5), y_range=(-5, 5), filename="output", **kwargs):
        super().__init__(**kwargs)
        self.equation = equation
        self.x_range = x_range
        self.y_range = y_range
        self.custom_filename = filename

    def construct(self):
        # # Set custom filename BEFORE rendering starts
        # self.renderer.file_writer.output_file = self.custom_filename

        # Define symbols
        x, y = sp.symbols('x y')

        # Convert equation to LaTeX for display
        equation_latex = sp.latex(sp.Eq(self.equation, 0))

        # Create Axes
        axes = Axes(
            x_range=[self.x_range[0], self.x_range[1], 1],
            y_range=[self.y_range[0], self.y_range[1], 1],
            axis_config={"color": WHITE}
        )
        self.play(Create(axes))

        # Determine if function is explicit (y in terms of x) or implicit
        if y in self.equation.free_symbols:
            # Implicit equation: Plot using `plot_implicit_curve`
            implicit_graph = axes.plot_implicit_curve(
                lambda x_val, y_val: sp.lambdify((x, y), self.equation, "numpy")(x_val, y_val),
                color=BLUE
            )
            self.play(Create(implicit_graph), run_time=2)

        else:
            # Explicit function: Solve for y and plot using `plot`
            y_solution = sp.solve(self.equation, y)
            if y_solution:
                explicit_func = sp.lambdify(x, y_solution[0], 'numpy')
                graph = axes.plot(explicit_func, color=BLUE)
                self.play(Create(graph), run_time=5)

        # Display the equation as text
        equation_text = MathTex(equation_latex, color=WHITE)
        equation_text.to_corner(UL)
        self.play(Write(equation_text))

        self.wait(2)

# 🟢 Example Usage - This will work for both explicit and implicit functions!
if __name__ == "__main__":
    x, y, h, k, r = sp.symbols('x y h k r')

    # Example 1: Circle
    circle_eq = (x - 0)**2 + (y - 0)**2 - 5
    with tempconfig({"output_file": "circle_output"}):
        scene = GeneralFunctionPlot(circle_eq)
        scene.render()

    # Example 2: Parabola
    parabola_eq = y - x**2
    with tempconfig({"output_file": "parabola_output"}):
        scene = GeneralFunctionPlot(parabola_eq)
        scene.render()