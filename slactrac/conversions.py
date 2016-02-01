import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import scipy.constants as _spc


def gamma2GeV(gamma):
    """
    Finds the energy in GeV of an electron with relativistic Lorentz factor :math:`\\gamma`.

    Parameters
    ----------

    gamma : float
        Relativistic Lorentz factor :math:`\\gamma`.
    """
    n_pts = _np.size(gamma)
    if n_pts > 1:
        for i, val in enumerate(gamma):
            gamma[i] = gamma2GeV(val)
        return gamma
    else:
        gamma = _np.float(gamma)
        return gamma * ( _spc.m_e * (_spc.c**2) / (_spc.eV * _spc.giga) )


def GeV2gamma(E):
    """
    Finds the relativistic Lorentz factor :math:`\\gamma` of an electron from a given energy.

    Parameters
    ----------

    E : float
        Electron energy in GeV.
    """
    if _np.size(E) == 1:
        E = _np.float(E)
    else:
        E = _np.array(E, dtype='float')
    return E / ( _spc.m_e * (_spc.c**2) / (_spc.eV * _spc.giga) )


def GeV2joule(E):
    """
    Converts energy from units of GeV to joules.

    Parameters
    ----------

    E : float
        Energy in GeV.
    """
    return eV2joule(E) * _spc.giga


def eV2joule(E):
    """
    Converts energy from units of eV to joules.

    Parameters
    ----------

    E : float
        Energy in eV.
    """
    if _np.size(E) == 1:
        E = _np.float(E)
    else:
        E = _np.array(E, dtype='float')

    return E * _spc.eV
