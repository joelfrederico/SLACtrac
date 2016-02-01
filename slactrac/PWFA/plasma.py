import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
    import slactrac as _sltr
    import periodictable as _pt
    import scipy.constants as _spc
else:
    import unittest.mock as _mock
    _pt = _mock.MagicMock()


class Plasma(object):
    """
    A class for relating plasma density to plasma frequency :math:`\\omega_p` and ion focusing force.

    Input plasma density either `n_p` in SI units, or `n_p_cgs` in CGS units.

    Parameters
    ----------

    n_p : float
        Plasma density in SI units.
    n_p_cgs : float
        Plasma density in CGS units.
    species : periodictable.core.Element
        The species of gas used (see :class:`periodictable.core.Element`).
    """
    def __init__(self, n_p=None, n_p_cgs=None, species=_pt.hydrogen):
        if species is None:
            species = _pt.H
        # ============================
        # Reconcile n_p, n_p_cgs
        # ============================
        if n_p is None and n_p_cgs is None:
            raise ValueError('Keywords n_p and n_p_cgs cannot both be None')
        elif n_p is not None and n_p_cgs is not None:
            raise ValueError('Keywords n_p and n_p_cgs cannot both be specified')
        elif n_p is not None:
            self.n_p = n_p
        elif n_p_cgs is not None:
            self.n_p_cgs = n_p_cgs

        if type(species) != _pt.core.Element:
            raise TypeError('Input species must be derived from periodictable package.')
        else:
            self._species = species

    @property
    def species(self):
        """
        Species used in plasma.
        """
        return self._species

    @property
    def m(self):
        """
        Mass of the ion in AMU.
        """
        return self._species.mass * _spc.m_u

    @property
    def E_rest(self):
        """
        Rest energy of the plasma ion.
        """
        return self.m * _spc.c**2

    @property
    def n_p(self):
        """
        Plasma density in SI units.
        """
        return self._n_p

    @n_p.setter
    def n_p(self, n_p):
        self._n_p = n_p

    @property
    def w_p(self):
        """
        Plasma frequency :math:`\\omega_p` for given plasma density
        """
        return _np.sqrt(self.n_p * _np.power(_spc.e, 2) / (_spc.m_e * _spc.epsilon_0))

    def k_ion(self, E):
        """
        Geometric focusing force due to ion column for given plasma density as a function of *E*
        """
        return self.n_p * _np.power(_spc.e, 2) / (2*_sltr.GeV2joule(E) * _spc.epsilon_0)

    def beta_matched(self, E):
        return 1/_np.sqrt(self.k_ion(E))

    @property
    def n_p_cgs(self):
        """
        Plasma density in CGS units
        """
        return self.n_p * 1e-6

    @n_p_cgs.setter
    def n_p_cgs(self, n_p_cgs):
        self.n_p = n_p_cgs * 1e6
