import sympy as sp

# Define a symbol
x = sp.symbols('x')

# Define an equation
equation = sp.Eq(x**2 - 4, 0)

# Solve the equation
solutions = sp.solve(equation, x)

# Print the solutions
print("Solutions to the equation x^2 - 4 = 0:")
for sol in solutions:
    print(sol)