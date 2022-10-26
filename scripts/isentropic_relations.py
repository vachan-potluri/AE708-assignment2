import scipy.optimize

def area_ratio_vs_M(M, gamma=1.4):
    # area ratio as a function of Mach number
    return (0.5*(gamma+1))**(-0.5*(gamma+1)/(gamma-1)) * (
        1 + 0.5*(gamma-1)*M**2)**(0.5*(gamma+1)/(gamma-1)
    ) / M

def T_ratio_vs_M(M, gamma=1.4):
    return (1+0.5*(gamma-1)*M**2)

def p_ratio_vs_M(M, gamma=1.4):
    return (T_ratio_vs_M(M, gamma))**(gamma/(gamma-1))

def rho_ratio_vs_M(M, gamma=1.4):
    return (T_ratio_vs_M(M, gamma))**(1/(gamma-1))

epsilon = 4 # exit area to throat area ratio
def f(M, gamma=1.4): return area_ratio_vs_M(M) - epsilon # the function to find roots
M_e = scipy.optimize.fsolve(f, epsilon**0.5)[0]
print("Exit area ratio: {:.3e}\nMach number: {:.3e}".format(epsilon, M_e))
print("Stagnation temperature, pressure and density ratios:\n{:.3e}\n{:.3e}\n{:.3e}".format(
    T_ratio_vs_M(M_e),
    p_ratio_vs_M(M_e),
    rho_ratio_vs_M(M_e)
))
