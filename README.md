# ACEPython - An equilibrium chemistry code

<p align="center"><b><a href="#introduction">Introduction</a> | <a href="#usage">Usage</a> | <a href="#taurex3">TauREx 3</a> | <a href="#citing-pdfo">Citing ACEPython</a></b></p>


## Introduction

ACEPython is a Python wrapper for the FORTRAN equilibrium chemistry code developed by [Agúndez et al. 2012](https://ui.adsabs.harvard.edu/abs/2012A%26A...548A..73A/abstract). It can rapidly compute the equilibirum chemical scheme for a given temperature and pressure.

### Installation

ACEPython can be installed with prebuilt wheels using pip:

```bash
pip install acepython
```

Or, if you prefer, you can build it from source which requires a FORTRAN and C compiler. The following commands will build and install ACEPython:

```bash
git clone https://github.com/ucl-exoplanets/acepython.git
cd acepython
pip install .
```

## Usage

ACEPython can be used to compute the equilibrium chemistry for a given temperature and pressure. Temperature and pressure must be created with astropy units. For pressure, any unit can be used (Pa, bar etc). The following example shows how to compute the equilibrium chemistry for a column of atmosphere:

```python
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

ax1.set_yscale("log")
ax1.set_xscale("log")
ax1.invert_yaxis()
ax1.set_ylabel("Pressure (bar)")
ax1.set_xlabel("VMR")

ax1.legend()

ax2.plot(mu_profile, pressure)
ax2.set_yscale("log")
ax2.invert_yaxis()
ax2.set_ylabel("Pressure (bar)")
ax2.set_xlabel("Mean molecular weight (au)")

plt.show()
```

Should produce the following figure:
![alt text](https://github.com/ucl-exoplanets/acepython/blob/main/examples/ace_example.svg?raw=true)

### Custom chemical scheme

By default the elements in the chemical scheme are <mark>H, He, C, N, O</mark> at log abundances <mark>12, 10.93, 8.39, 7.86, 8.73</mark> respectively. The abundances can be changed by passing the elements and corresponding abundances to the `run_ace` function:

```python
species, mix_profile, mu_profile = run_ace(
    temperature,
    pressure,
    elements=["H", "He", "C", "N", "O"],
    abundances=[12, 10.93, 8.39, 7.86, 7.73],
)
```

where we have changed *O* to have a log abundance of *7.73*.

You can customize the species included by passing in thermochemical and species data files.

For example, if we have a custom thermochemical data file called `custom_thermochemical_data.dat` and a custom species data file called `custom_species_data.dat` that includes sulphur we can run ACEPython with:

```python
species, mix_profile, mu_profile = run_ace(
    temperature,
    pressure,
    elements=["H", "He", "C", "N", "O", "S"],
    abundances=[12, 10.93, 8.39, 7.86, 7.73, 7.0],
    thermochemical_data="custom_thermochemical_data_w_S.dat",
    species_data="custom_species_data_w_S.dat",
)
```

## TauREx3

ACEPython also includes a plugin for [TauREx 3.1](https://taurex3-public.readthedocs.io/en/latest/) that allows you to use ACEPython as a chemistry scheme. In the input file you can select it in the *Chemistry* section using <mark>acepython</mark> with arguments:

```bash
[Chemistry]
chemistry = acepython
# He/H ratio (optional)
he_h_ratio = 0.83
# Elements excluding H, He (optional)
elements = C, N, O  
# log abundances (optional)
abundances = 8.39, 7.86, 8.73 
# Custom species data file (optional)
spec_file = custom_species_data.dat 
# Custom thermochemical data file (optional)
thermo_file = custom_thermochemical_data.dat 
```

## Citing ACEPython

If you use ACEPython in your research, please cite the following papers:

```bibtex
@ARTICLE{Agundez2012,
    author = {{Ag{\'u}ndez}, M. and {Venot}, O. and {Iro}, N. and {Selsis}, F. and
        {Hersant}, F. and {H{'e}brard}, E. and {Dobrijevic}, M.},
        title = "{The impact of atmospheric circulation on the chemistry of the hot Jupiter HD 209458b}",
    journal = {A\&A},
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

@ARTICLE{2021ApJ...917...37A,
       author = {{Al-Refaie}, A.~F. and {Changeat}, Q. and {Waldmann}, I.~P. and {Tinetti}, G.},
        title = "{TauREx 3: A Fast, Dynamic, and Extendable Framework for Retrievals}",
      journal = {\apj},
     keywords = {Open source software, Astronomy software, Exoplanet atmospheres, Radiative transfer, Bayesian statistics, Planetary atmospheres, Planetary science, 1866, 1855, 487, 1335, 1900, 1244, 1255, Astrophysics - Instrumentation and Methods for Astrophysics, Astrophysics - Earth and Planetary Astrophysics},
         year = 2021,
        month = aug,
       volume = {917},
       number = {1},
          eid = {37},
        pages = {37},
          doi = {10.3847/1538-4357/ac0252},
archivePrefix = {arXiv},
       eprint = {1912.07759},
 primaryClass = {astro-ph.IM},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2021ApJ...917...37A},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}

@ARTICLE{2022ApJ...932..123A,
       author = {{Al-Refaie}, A.~F. and {Changeat}, Q. and {Venot}, O. and {Waldmann}, I.~P. and {Tinetti}, G.},
        title = "{A Comparison of Chemical Models of Exoplanet Atmospheres Enabled by TauREx 3.1}",
      journal = {\apj},
     keywords = {Open source software, Publicly available software, Chemical abundances, Bayesian statistics, Exoplanet atmospheres, Exoplanet astronomy, Exoplanet atmospheric composition, Exoplanets, Radiative transfer, 1866, 1864, 224, 1900, 487, 486, 2021, 498, 1335, Astrophysics - Earth and Planetary Astrophysics, Astrophysics - Instrumentation and Methods for Astrophysics},
         year = 2022,
        month = jun,
       volume = {932},
       number = {2},
          eid = {123},
        pages = {123},
          doi = {10.3847/1538-4357/ac6dcd},
archivePrefix = {arXiv},
       eprint = {2110.01271},
 primaryClass = {astro-ph.EP},
       adsurl = {https://ui.adsabs.harvard.edu/abs/2022ApJ...932..123A},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```
