import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from isentropic_relations import area_ratio_vs_M, p_ratio_vs_M
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "Times",
    "font.size": 8,
    "axes.formatter.limits": [-2,2]
})

def savefig(fig, directory, basename, formats=["png", "pdf"]):
    # saves a given figure handle in <directory> as <basename>.png and <basename>.pdf
    for fmt in formats:
        fullname = "{}/{}.{}".format(directory, basename, fmt)
        fig.savefig(fullname, format=fmt)
        print("Written {}".format(fullname))

def get_area_ratio(x, diffuser_type="conical"):
    # gives throat area ratio at a x-location for the three nozzles considered
    R_t = 1
    Rc_div = 0.4*R_t # curvature radius just after throat
    Rc_conv = 1.5*R_t
    if diffuser_type == "conical":
        theta_n = 15*np.pi/180 # angle at point N
        x_n  = 0.4*R_t*np.sin(theta_n) # x coordinate of point N
        y_n = R_t + 0.4*R_t*(1-np.cos(theta_n)) # y coordinate of point N
        if x < 0:
            # converging section
            theta = np.arcsin(-x/Rc_conv)
            y = R_t + Rc_conv*(1-np.cos(theta))
        elif x < x_n:
            # circular arc after diverging section
            theta = np.arcsin(x/Rc_div)
            y = R_t + Rc_div*(1-np.cos(theta))
        else:
            y = y_n + (x-x_n)*np.tan(theta_n)
        return (y/R_t)**2
    elif diffuser_type == "rao_K0.6" or diffuser_type == "rao_K0.8":
        theta_n = 30*np.pi/180 # angle at point N
        x_n  = 0.4*R_t*np.sin(theta_n) # x coordinate of point N
        y_n = R_t + 0.4*R_t*(1-np.cos(theta_n)) # y coordinate of point N

        if diffuser_type == "rao_K0.6":
            parabola_coeffs = [4.466e-01, 7.910e-01, -1.129e+00]
        else:
            parabola_coeffs = [1.280e+00, -9.650e-01, -2.041e-01]
        
        if x < 0:
            # converging section
            theta = np.arcsin(-x/Rc_conv)
            y = R_t + Rc_conv*(1-np.cos(theta))
        elif x < x_n:
            # circular arc after diverging section
            theta = np.arcsin(x/Rc_div)
            y = R_t + Rc_div*(1-np.cos(theta))
        else:
            y = 0.5*(
                    -parabola_coeffs[1] +
                    np.sqrt(parabola_coeffs[1]**2 - 4*parabola_coeffs[0]*(parabola_coeffs[2]-x))
                )/parabola_coeffs[0]
        return (y/R_t)**2
    else:
        assert False, "Incorrect diffuser type"

indices = ["conical", "rao_K0.6", "rao_K0.8"]
data_files = pd.Series(
    [
        "../run/conical/data/axis_data.csv",
        "../run/rao2_K0.6/data/axis_data.csv",
        "../run/rao2_K0.8/data/axis_data.csv"
    ],
    indices
)
plot_labels = pd.Series(["Conical", "Rao, $K=0.6$", "Rao, $K=0.8$"], indices)
plot_styles = pd.Series(["r-", "b--", "g-."], indices)

fig1, axes1 = plt.subplots(3,1) # p, T and M vs X
fig1.set_size_inches(4,7)
variables = ["p", "T", "Ma"]
var_subaxes_id = pd.Series([0,1,2], variables) # index within axes1 where variables are plotted
var_axis_label = pd.Series([r"$p$ [Pa]", r"$T$ [K]", r"$M$"], variables)
for idx in indices:
    data = pd.read_csv(data_files.loc[idx])
    for var in variables:
        axes1[var_subaxes_id.loc[var]].plot(
            data["Points:0"],
            data[var],
            plot_styles.loc[idx],
            label=plot_labels.loc[idx]
        )

for var in variables:
    ax = axes1[var_subaxes_id.loc[var]]
    ax.grid()
    ax.legend()
    ax.set_ylabel(var_axis_label.loc[var])
    ax.set_xlabel(r"$x$ [m]")
fig1.tight_layout(pad=0.5)
savefig(fig1, "../plots", "pTM_vs_x")

fig2, axes2 = plt.subplots(2,1) # M and p vs A/At
fig2.set_size_inches(4,5)
variables = ["Ma", "p"]
var_subaxes_id = pd.Series([0,1], variables)
var_axis_label = pd.Series([r"$M$", r"$p$ [Pa]"], variables)
for idx in indices:
    data = pd.read_csv(data_files.loc[idx])
    x = data["Points:0"]
    area_ratio = np.ones_like(x)
    for i,cur_x in enumerate(x):
        area_ratio[i] = get_area_ratio(cur_x, idx)
    for var in variables:
        axes2[var_subaxes_id.loc[var]].plot(
            area_ratio,
            data[var],
            plot_styles.loc[idx],
            label=plot_labels.loc[idx]
        )
# add isentropic variations
M = np.linspace(0.2, 3)
axes2[var_subaxes_id.loc["Ma"]].plot(area_ratio_vs_M(M), M, "m:", label="Isentropic")
axes2[var_subaxes_id.loc["p"]].plot(area_ratio_vs_M(M), 287/p_ratio_vs_M(M), "m:", label="Isentropic")

for var in variables:
    ax = axes2[var_subaxes_id.loc[var]]
    ax.grid()
    ax.legend()
    ax.set_ylabel(var_axis_label.loc[var])
    ax.set_xlabel(r"$A/A_t$")
fig2.tight_layout(pad=0.5)
savefig(fig2, "../plots", "Mp_vs_area_ratio")
plt.show()
    