"""Tests ace package."""

import pytest


def test_run_ace():
    """Tests ace to see if it runs."""
    from acepython import run_ace
    from astropy import units as u
    import numpy as np

    temperature = np.linspace(3000, 1000, 100) << u.K
    pressure = np.logspace(6, -2, 100) << u.bar

    species, mix_profile, mu_profile = run_ace(
        temperature,
        pressure,
    )

    assert mix_profile.shape[-1] == pressure.shape[-1]
    assert mu_profile.shape[-1] == pressure.shape[-1]

    np.testing.assert_array_almost_equal(np.sum(mix_profile, axis=0), 1.0)


# test if taurex installed
# if not, skip the test


# @pytest.mark.skip(reason="This test is not yet implemented.")
def test_taurex3():
    """Tests taurex3 to see if it runs."""
    taurex = pytest.importorskip("taurex")

    from acepython.taurex3 import ACEChemistry
    from astropy import units as u
    import numpy as np

    temperature = np.linspace(3000, 1000, 100)
    pressure = np.logspace(6, -2, 100)

    tau = ACEChemistry()
    tau.initialize_chemistry(temperature_profile=temperature, pressure_profile=pressure)

    assert tau.mixProfile.shape[-1] == pressure.shape[-1]
    assert tau.muProfile.shape[-1] == pressure.shape[-1]


def test_taurex3_c_ratio():
    """Tests taurex3 to see if it runs."""
    taurex = pytest.importorskip("taurex")

    from acepython.taurex3 import ACEChemistry
    from astropy import units as u
    import numpy as np

    temperature = np.linspace(3000, 1000, 100)
    pressure = np.logspace(6, -2, 100)

    tau = ACEChemistry(C_ratio=0.5)
    tau.initialize_chemistry(temperature_profile=temperature, pressure_profile=pressure)
    assert tau._ratios[0] == 0.5
    assert tau.mixProfile.shape[-1] == pressure.shape[-1]
    assert tau.muProfile.shape[-1] == pressure.shape[-1]
