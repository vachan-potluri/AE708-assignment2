# See https://moodle.iitb.ac.in/pluginfile.php/336817/mod_assign/introattachment/0/Bell_nozzle_design_methodology.pdf?forcedownload=1

import numpy as np
import matplotlib.pyplot as plt

# Parameters
R_t = 1 # throat radius
epsilon = 4 # exit area to throat area ratio
R_e = R_t*(epsilon**0.5) # exit radius
theta_n = 30*np.pi/180 # initial nozzle contour angle after circular segment
Rc_div = 0.4*R_t # curvature radius after divergent section
x_n = Rc_div*np.sin(theta_n) # x coordinate of point N (x axis starts at throat)
y_n = R_t + Rc_div*(1-np.cos(theta_n)) # y coordinate of point N (y axis starts from nozzle axis)
theta_conical = 15*np.pi/180
L_conical = (R_e-R_t)/np.tan(theta_conical) # conical nozzle length with 15 degree cone angle
K = 0.8 # length of Rao nozzle relative to conical nozzle with 15 degree cone angle

# Solve for coefficients
coeff_matrix = np.array([
    [2*y_n, 1, 0],
    [R_e**2, R_e, 1],
    [y_n**2, y_n, 1]
])
rhs_vector = np.array([1/np.tan(theta_n), K*L_conical, x_n])
solution = np.linalg.solve(coeff_matrix, rhs_vector)
np.set_printoptions(formatter={'float': '{: 0.3e}'.format})
print("Solution coefficients: {}".format(solution))

# Plot for comparison
L_rao = solution[0]*R_e**2 + solution[1]*R_e + solution[2] # length of Rao nozzle
fig, ax = plt.subplots(1,1)
y = np.linspace(y_n, R_e)
x_rao = solution[0]*y**2 + solution[1]*y + solution[2]
x_conical = (y-y_n)/np.tan(theta_conical) + x_n
ax.plot(x_rao, y, "b-", label="Rao")
ax.plot(x_conical, y, "r--", label="Conical")
ax.grid()
ax.legend()
plt.show()

# Data output (from the point N to the exit)
## pre-throat: circular arc profile
## post-throat: smaller circular arc followed by conical/rao profile
# np.savetxt("rao_profile.dat", np.vstack((x_rao, y)).T)
