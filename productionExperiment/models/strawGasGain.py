import numpy as np
import matplotlib.pyplot as plt

#Using Diethorn's formula (eqn 4.14 from Blum, Drift Chambers)

#Define parameters
wire_radius = 200.e-6
straw_inner_radius = 2.5e-3

#Convert to symbols used in text book
a = wire_radius
b = straw_inner_radius


#
# Determine constant
#

#See Blum p.135 (just below eqn 4.14)

wire_voltages_used = np.array([1600.,1650.,1700.])
measured_gain = np.array([1.e5,2.e5,3.8e5])

ln_b_over_a = np.log(b/a)
rho_over_rho0 = 1. #Assuming operating at rho0
V = wire_voltages_used
G = measured_gain

y = ( np.log(G) * ln_b_over_a ) / V
x = np.log( V / ( ln_b_over_a * a  * rho_over_rho0 ) )

pfit, stats = np.polynomial.Polynomial.fit( x, y, 1, full=True, window=(np.min(x),np.max(x)), domain=(np.min(x),np.max(x)) )
gradient = stats[0]
intercept = stats[1]
'''
plt.scatter(x,y,marker="o",color="blue",label="Measurements")
plt.plot( x, pfit(x), color='red', linestyle="--", label=r"Fit: $y = %0.3g x + %0.3g$"%(gradient,intercept) )

plt.legend()
plt.grid()

plt.show()
'''


#
# Extrapolate data to all voltages
#

#TODO Really shoudl have 2 constants
constant = gradient
E_min = 50. * 1.e3  / 1.e-2
delta_V = 23.

wire_voltage_space = np.linspace(1000.,2000.,num=100)
V = wire_voltage_space

gain_values = 1.e6 * np.exp( ( (np.log(2) * V ) / ( ln_b_over_a * delta_V ) ) * np.log( V / ( ln_b_over_a * a * E_min * rho_over_rho0 ) ) )

plt.scatter(wire_voltage_space,gain_values,marker=".",color="green",label="Extrapolated")
plt.legend()
plt.grid()
plt.yscale('log')
plt.xlabel("Wire voltage [V]")
plt.ylabel("Gain")

plt.show()