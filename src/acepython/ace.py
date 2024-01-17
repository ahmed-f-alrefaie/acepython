from .mdace import md_ace as acef

import numpy as np
from astropy import units as u
import typing as t
import importlib.resources as ires


class AceError(Exception):
    def __init__(self, error_code: int):
        codes = {
            1: "Number of elements too high",
            2: "Unknown therm data type",
            3: "Many elements in species",
            4: "Error on elements.",
            8: "Error searching for thermo data",
            5: "Number of atoms zero in species",
            6: "Wrong number of atoms in species",
            7: "Species duplicated.",
            9: "Missing (+/-) charged species",
            15: "Element not found in element list",
        }

        super().__init__(codes.get(error_code, "Unknown error"))


def run_ace(
    temperature: u.Quantity,
    pressure: u.Quantity,
    elements: t.Optional[t.List[str]] = ["H", "He", "C", "N", "O"],
    abundances: t.Optional[t.List[float]] = [12, 10.93, 8.39, 7.86, 8.73],
    specfile: t.Optional[str] = None,
    thermfile: t.Optional[str] = None,
) -> np.ndarray:
    """Runs ACE on a given temperature and pressure profile.

    Args:
        temperature: Temperature profile.
        pressure: Pressure profile.
        He_solar: Solar helium abundance in dex, default is 10.93.
        C_solar: Solar carbon abundance in dex, default is 8.39.
        O_solar: Solar oxygen abundance in dex, default is 8.73.
        N_solar: Solar nitrogen abundance in dex, default is 7.86.
        specfile: Path to the ACE specfile.
        thermfile: Path to the ACE thermfile.

    """

    specfile = specfile or ires.files("acepython") / "data" / "composes.dat"
    thermfile = thermfile or ires.files("acepython") / "data" / "NASA.therm"

    with open(specfile, "r") as f:
        species = [s.split()[1].strip() for s in f]
    with open(specfile, "r") as f:
        molar_masses = np.array([float(l.split()[2].strip()) for l in f]) << u.u

    # Pad elements to 2 characters
    elements = [e.ljust(2) for e in elements]
    element_array = np.empty(len(elements), dtype="S2")
    for i, element in enumerate(elements):
        element_array[i] = element
    mix_profile, error_code = acef.ace(
        len(species),
        str(specfile),
        str(thermfile),
        np.zeros_like(pressure.value),
        pressure.to(u.bar).value,
        temperature.to(u.K).value,
        element_array,
        np.array(abundances),
    )
    if error_code != 0:
        raise AceError(error_code)

    # Normalize the mixing ratios
    mix_profile = mix_profile / mix_profile.sum(axis=0, keepdims=True)

    mu_profile = (mix_profile * molar_masses[:, None]).sum(axis=0)

    return species, mix_profile, mu_profile
