from acepython import run_ace
from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt


temperature = np.linspace(3000, 1000, 100) << u.K
pressure = np.logspace(6, -2, 100) << u.bar

species, mix_profile, mu_profile = run_ace(
    temperature,
    pressure,
)

species_to_see = ["H2", "H20", "CH4", "NH3", "C2H2", "CO", "CO2", "H2CO"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

for i, spec in enumerate(species):
    if spec in species_to_see:
        ax1.plot(mix_profile[i], pressure, label=spec)

ax1.set_title("Chemical composition")
ax1.set_yscale("log")
ax1.set_xscale("log")
ax1.invert_yaxis()
ax1.set_ylabel("Pressure (bar)")
ax1.set_xlabel("VMR")

ax1.legend()
ax2.set_title("Mean molecular weight")
ax2.plot(mu_profile, pressure)
ax2.set_yscale("log")
ax2.invert_yaxis()
ax2.set_ylabel("Pressure (bar)")
ax2.set_xlabel("Mean molecular weight (au)")

plt.savefig("ace_example.svg")
