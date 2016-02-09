import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np

from .baseclass import baseclass as _baseclass
import warnings as _warnings
from .conversions import *


class Scatter(_baseclass):
    """
    Represents a foil element that scatters the beam.

    Parameters
    ----------

    thickness : float
        The thickness of the foil in SI units.
    radlength : float
        The radiation lenght of the foil.
    name : str
        The name used to identify the element.
    verbose : boolean
        Whether or not to print information to the terminal
    """
    _type = 'scatter'
    _order = 1

    def __init__(self, thickness=0, radlength=1, name=None, verbose=False):
        self.name   = name
        self.verbose = verbose
        self._x      = thickness
        self._X0     = radlength

    @property
    def thickness(self):
        return self._x

    @property
    def radlength(self):
        return self._X0

    def theta_rms(self, energy_GeV):
        """
        The RMS scattering angle in radians.
        """
        x_div_X0 = self._x/self._X0
        theta = 13.6e-3/energy_GeV * _np.sqrt(x_div_X0) * (1+0.038*_np.log(x_div_X0))
        return theta
    # theta_rms = property(_get_theta_rms)

    @property
    def R(self):
        """
        This is necessary for the simulation, but a scattering element does not have an R matrix, and this is the identity.
        """
        _warnings.warn('This scatter element does not have an R matrix: returning identity instead', UserWarning, stacklevel=3)
        return _np.identity(6)

    def change_E(self, old_gamma, new_gamma):
        """
        Changes the energy of the element.
        """
        pass

    @property
    def ele_name(self):
        """
        Returns the elegant-styled name.
        """
        name = 'SCATTER_{}_{ind:03.0f}'.format(self.name, self.ind)
        return name

    @property
    def ele_string(self, ind, gamma):
        """
        Returns the full elegant entry.
        """
        string = (
            '{name}\t:SCATTER , &\n'
            '\t\tXP = {xp}    , &\n'
            '\t\tYP = {yp}'
            ).format(
                name = self.elename,
                xp   = self.theta_rms(gamma2GeV(gamma)),
                yp   = self.theta_rms(gamma2GeV(gamma))
                )
        string = string + self._kwargs_str

        return string
