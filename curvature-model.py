import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial as Poly

# Computes the lagrange polynomial for (x_i, y_i)
def lagrange_interpolate(x, y):
	if len(x) <= len(y):
		k = len(x) - 1
	else:
		k = len(y) - 1

	min_x = min(x)
	max_x = max(x)
	result = Poly([0],[min_x,max_x],[min_x,max_x]) # Initializing P(x) = 0

	for j in range(0,k+1):
		numerator = Poly([1],[min_x,max_x],[min_x,max_x])
		denominator = 1.0
		for m in range(0,k+1):
			if m != j:
				numerator *= Poly([-x[m],1],[min_x,max_x],[min_x,max_x])
				denominator *= x[j]-x[m]
		result += (numerator/denominator)*y[j]

	print(result)
	return result


def main():
	np.random.seed(11)
	x = np.linspace(0, 100, 20)
	y = np.random.normal(50, 1000, x.shape)
	plt.plot(x, y, 'o')

	p = lagrange_interpolate(x,y)

	p_x, p_y = p.linspace()
	plt.plot(p_x, p_y, lw=2)

	plt.show()
if __name__ == '__main__':
	main()
