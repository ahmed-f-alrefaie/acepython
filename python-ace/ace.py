from .mdace import md_ace as acef

import numpy as np
import math
import pkg_resources
from astropy import units as u

def run_ace(
        temperature: u.Quantity,
        pressure: u.Quantity,
        He_solar: float = 10.93,
        C_solar: float = 8.39,
        O_solar: float = 8.73,
        N_solar: float = 7.86,
) -> np.ndarray:
    """Run Ace"""

    specfile = pkg_resources.resource_filename('python_ace','data/composes.dat')
    thermfile = pkg_resources.resource_filename('python_ace','data/NASA.therm')


    with open(specfile,'r') as f:
        species = [l.split()[1].strip() for l in f if not l.split()[1].strip().endswith('c')]
    with open(specfile,'r') as f:
        molar_masses = np.array([float(l.split()[2].strip()) for l in f]) << u.u

    mix_profile = acef.ace(len(species),specfile,
                                 thermfile,
                                 np.zeros_like(pressure.value),
                                 pressure.to(u.bar).value,
                                 temperature.to(u.K).value,
                                 He_solar,
                                 C_solar,
                                 O_solar,
                                 N_solar)

    mu_profile = (mix_profile*molar_masses[:,None]).sum(axis=0)

    return species, mix_profile, mu_profile

