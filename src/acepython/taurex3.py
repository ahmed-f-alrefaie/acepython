import typing as t

try:
    from taurex.chemistry import AutoChemistry
except ImportError:
    AutoChemistry = object  # Make it a dummy class

import numpy as np
import importlib.metadata as meta
import math
from astropy import units as u
from .ace import run_ace
from taurex.core import fitparam
import pathlib


class ACEChemistry(AutoChemistry):
    """ACE Chemistry for TauREx3."""

    DEFAULT_ELEMENTS = ["C", "N", "O"]
    DEFAULT_ABUNDANCES = [8.39, 7.86, 8.73]

    def __init__(
        self,
        he_h_ratio: t.Optional[float] = 0.083,
        elements: t.List[str] = None,
        abundances: t.List[float] = None,
        specfile: t.Optional[str] = None,
        thermfile: t.Optional[str] = None,
        ratio_element: t.Optional[str] = "O",
        metallicity: t.Optional[float] = 1.0,
    ):
        """ACE Chemistry for TauREx3.

        Args:
            elements: List of elements to use. Defaults to ["H", "He", "C", "N", "O"].
            abundances: List of abundances in dex to use. Defaults to [12, 10.93, 8.39, 7.86, 8.73].
            specfile: Path to the ACE specfile. Defaults to inbuilt.
            thermfile: Path to the ACE thermfile. Defaults to inbuilt.
            ratio_element: Element to use for ratio. Defaults to 'O'.
        """
        super().__init__(self.__class__.__name__)

        elements = elements or self.DEFAULT_ELEMENTS
        abundances = abundances or self.DEFAULT_ABUNDANCES

        # Filter out H and He as they are determined by ratio
        elements, abundances = zip(
            *[
                (ele, abu)
                for ele, abu in zip(elements, abundances)
                if ele not in ["H", "He"]
            ]
        )

        self._elements = elements
        self._abundances = abundances
        self._metallicity = metallicity
        self.he_h_ratio = he_h_ratio
        self.spec_file = specfile

        self.thermfile = thermfile

        self.ratio_element = ratio_element

        metal_elements, metal_abundances = zip(
            *[
                (ele, abu)
                for ele, abu in zip(self._elements, self._abundances)
                if ele not in ["H", "He", ratio_element]
            ]
        )

        self.metal_elements = metal_elements
        self.metal_abundances = metal_abundances

        self.ratio_abundance = self._abundances[
            self._elements.index(self.ratio_element)
        ]

        self._ratios: np.ndarray = 10 ** (
            np.array(self.metal_abundances) - self.ratio_abundance
        )

        self.species = self._species()
        self.determine_active_inactive()
        self.add_ratio_params()

    def add_ratio_params(self):
        for idx, element in enumerate(self.metal_elements):
            if element == self.ratio_element:
                continue
            param_name = f"{element}_{self.ratio_element}_ratio"
            param_tex = f"{element}/{self.ratio_element}"

            def read_mol(self, idx=idx):
                return self._ratios[idx]

            def write_mol(self, value, idx=idx):
                self._ratios[idx] = value

            read_mol.__doc__ = f"Equilibrium {element}/{self.ratio_element} ratio."
            write_mol.__doc__ = f"Equilibrium {element}/{self.ratio_element} ratio."
            fget = read_mol
            fset = write_mol

            bounds = [1.0e-12, 0.1]

            default_fit = False
            self.add_fittable_param(
                param_name, param_tex, fget, fset, "log", default_fit, bounds
            )

    def generate_elements_abundances(self):
        """Generates elements and abundances to pass into ace."""
        ratios = np.log10(self._ratios)
        ratio_abund = (
            math.log10(self._metallicity * (10 ** (self.ratio_abundance - 12))) + 12
        )

        metals = ratio_abund + ratios

        complete = np.array(
            [12, 12 + math.log10(self.he_h_ratio)] + [ratio_abund] + list(metals)
        )

        return ["H", "He"] + [self.ratio_element] + list(self.metal_elements), complete

    def _species(self):
        """Finds species in the ACE database."""
        with open(self.specfile, "r") as f:
            species = [s.split()[1].strip() for s in f if s]
        return species

    @property
    def gases(self):
        """Gases in the ACE database."""
        return self.species

    def initialize_chemistry(
        self,
        nlayers=100,
        temperature_profile=None,
        pressure_profile=None,
        altitude_profile=None,
    ):
        """Initializes the chemistry.

        Args:
            nlayers: Number of layers.
            temperature_profile: Temperature profile.
            pressure_profile: Pressure profile.
            altitude_profile: Altitude profile. (Deprecated)

        """
        elements, abundances = self.generate_elements_abundances()

        _, self._mix_profile, mu_profile = run_ace(
            temperature_profile << u.K,
            pressure_profile << u.Pa,
            elements=elements,
            abundances=abundances,
            specfile=self.specfile,
            thermfile=self.thermfile,
        )

        self.mu_profile = mu_profile.to(u.kg).value

    @property
    def mixProfile(self):
        """Mixing profile (VMR)."""
        return self._mix_profile

    @fitparam(
        param_name="metallicity",
        param_latex="Z",
        default_bounds=[0.2, 2.0],
        default_fit=False,
    )
    def metallicity(self):
        """Metallicity of the atmosphere."""
        return self._metallicity

    @metallicity.setter
    def metallicity(self, value):
        """Metallicity of the atmosphere."""
        self._metallicity = value

    @property
    def muProfile(self):
        """
        Molecular weight for each layer of atmosphere


        Returns
        -------
        mix_profile : :obj:`array`

        """
        return self.mu_profile

    @classmethod
    def input_keywords(cls):
        return [
            "ace",
            "acepython",
            "equilibrium",
        ]

    BIBTEX_ENTRIES = [
        """
        @ARTICLE{Agundez2012,
            author = {{Ag{\\'u}ndez}, M. and {Venot}, O. and {Iro}, N. and {Selsis}, F. and
                {Hersant}, F. and {H{\'e}brard}, E. and {Dobrijevic}, M.},
                title = "{The impact of atmospheric circulation on the chemistry of the hot Jupiter HD 209458b}",
            journal = {A\\&A},
            keywords = {astrochemistry, planets and satellites: atmospheres, planets and satellites: individual: HD 209458b, Astrophysics - Earth and Planetary Astrophysics},
                year = "2012",
                month = "Dec",
            volume = {548},
                eid = {A73},
                pages = {A73},
                doi = {10.1051/0004-6361/201220365},
        archivePrefix = {arXiv},
            eprint = {1210.6627},
        primaryClass = {astro-ph.EP},
            adsurl = {https://ui.adsabs.harvard.edu/abs/2012A&A...548A..73A},
            adsnote = {Provided by the SAO/NASA Astrophysics Data System}
        }
        """,
    ]
