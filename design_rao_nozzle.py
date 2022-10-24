# See https://moodle.iitb.ac.in/pluginfile.php/336817/mod_assign/introattachment/0/Bell_nozzle_design_methodology.pdf?forcedownload=1

import numpy as np
import matplotlib.pyplot as plt

# Parameters
R_t = 8e-3 # throat radius
epsilon = 5 # exit area to throat area ratio
R_e = R_t*(epsilon**0.5) # exit radius
theta_n = 15*np.pi/180 # initial nozzle contour angle after circular segment
theta_e = 8*np.pi/180 # nozzle contour angle at exit section
x_n = 0.382*R_t*np.sin(theta_n) # x coordinate of point N (x axis starts at throat)
y_n = R_t + 0.382*R_t*(1-np.cos(theta_n)) # y coordinate of point N (y axis starts from nozzle axis)

# Solve for coefficients
coeff_matrix = np.array([
    [2*y_n, 1, 0],
    [2*R_e, 1, 0],
    [y_n**2, y_n, 1]
])
rhs_vector = np.array([1/np.tan(theta_n), 1/np.tan(theta_e), x_n])
solution = np.linalg.solve(coeff_matrix, rhs_vector)
print("Solution coefficients: {}".format(solution))

# Plot for comparison
L = solution[0]*R_e**2 + solution[1]*R_e + solution[2] # length of the nozzle
fig, ax = plt.subplots(1,1)
y = np.linspace(y_n, R_e)
x_rao = solution[0]*y**2 + solution[1]*y + solution[2]
x_conical = (y-y_n)/np.tan(theta_n) + x_n
ax.plot(x_rao, y, "b-", label="Rao")
ax.plot(x_conical, y, "r--", label="Conical")
ax.grid()
ax.legend()
plt.show()

# Data output (from the point N to the exit)
## pre-throat: circular arc profile
## post-throat: smaller circular arc followed by conical/rao profile
# np.savetxt("rao_profile.dat", np.vstack((x_rao, y)).T)
