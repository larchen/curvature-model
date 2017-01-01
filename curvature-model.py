import numpy as np
import matplotlib.pyplot as plt

def discrete_curvature(f):

	k = np.zeros((1,f.shape[1]))

	for i in range(f.shape[1]-2):
		df_1 = f[:,i+1]-f[:,i]
		ds_1 = np.sqrt(sum(df_1**2))
		df_2 = f[:,i+2]-f[:,i+1]
		ds_2 = np.sqrt(sum(df_2**2))

		d2f = df_2/ds_2 - df_1/ds_1		# Difference between unit tangent vectors
		ds2 = (ds_2+ds_1)/2				# Approximate arclength

		curvature = np.sqrt(sum(d2f**2))/ds2

		k[0,i+1] = curvature
	print(k)
	return k


def main():
	t = np.linspace(0,100,1000)

	f = np.array([np.cos(t),np.sin(t),t])
	discrete_curvature(f)

	t = np.linspace(0,10,200)
	g = np.array([t**2,t])
	discrete_curvature(g)


if __name__ == '__main__':
	main()
