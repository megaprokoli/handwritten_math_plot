from matplotlib import pyplot
from parsing.math_function import MathFunction


exp = "0.1 * x ^ 4 - x ^ 2"    # f(-4) = 9,6
mf = MathFunction(exp.split(" "))

xy = mf.table([-4, 4, 1])

pyplot.plot(xy[0], xy[1])
pyplot.title("polynominal")
pyplot.xlabel("x")
pyplot.ylabel("y")

pyplot.show()
