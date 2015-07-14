import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np

from .driftmat import driftmat
from .baseclass import baseclass


class Quad(baseclass):
    """
    Represents a quadrupole with:

    * *length*: Length of the quad
    * *K1*: Geometric focusing strength of the quad
    * *order*: Order to calculate the transfer matrix
    * *name*: The name used to identify the quad
    """
    def __init__(self, length=0, K1=0, order=1, name=None, **kwargs):
        self.name   = name
        self._order  = int(order)
        self._type   = 'quad'
        self._length = _np.float64(length)
        self.K1      = _np.float64(K1)
        self._kwargs = kwargs

    @property
    def K1(self):
        """
        The geometric focusing strength.
        """
        return self._K1

    @K1.setter
    def K1(self, val):
        self._K1 = val

    @property
    def R(self):
        """
        The transfer matrix R for the quad.
        """
        return quadmat(L=self._length, K1=self.K1, order=self._order)

    @property
    def length(self):
        """
        The length of the quad.
        """
        return self._length

    def change_E(self, old_gamma, new_gamma):
        """
        Scale the setpoint energy of the magnet from the old energy old_gamma to new energy new_gamma.

        The best way to think about this is that the angle will change with different beam energy, so changing the beam energy changes the magnet’s properties, because the magnet’s B-field stays the same.
        """
        old_gamma = _np.float64(old_gamma)
        new_gamma = _np.float64(new_gamma)
        self.K1 *= old_gamma / new_gamma

    @property
    def ele_name(self):
        """
        Returns the elegant-styled name.
        """
        name = 'QUAD_{}_{:03.0f}'.format(self.name, self.ind)
        return name

    @property
    def ele_string(self):
        """
        Returns the full elegant entry.
        """
        string = '{}\t:KQUAD, L = {}, K1 = {}'.format(self.ele_name, self.length, self.K1)
        string = string + self._kwargs_str

        return string


def quadmat(K1=0, L=0, order=1):
    if ( K1 == 0 ):
        R = driftmat(L, order)
    else:
        rtK = _np.sqrt(_np.abs(K1))
        rtK_L = rtK * L
        sin_rtK_L = _np.sin(rtK_L)
        cos_rtK_L = _np.cos(rtK_L)
        sinh_rtK_L = _np.sinh(rtK_L)
        cosh_rtK_L = _np.cosh(rtK_L)
        R_f = _np.array(
            [[ cos_rtK_L    , sin_rtK_L/rtK ],
            [  -rtK*sin_rtK_L , cos_rtK_L   ]]
            )
        R_d = _np.array(
            [[ cosh_rtK_L   , sinh_rtK_L/rtK ],
            [  rtK*sinh_rtK_L , cosh_rtK_L   ]]
            )
        if ( K1 > 0 ):
            R = _np.zeros([6, 6])
            R[0:2, 0:2] = R_f
            R[2:4, 2:4] = R_d
            R[4:6, 4:6] = _np.identity(2)
        elif ( K1 < 0 ):
            R = _np.zeros([6, 6])
            R[0:2, 0:2] = R_d
            R[2:4, 2:4] = R_f
            R[4:6, 4:6] = _np.identity(2)
        else:
            print('Uhm who said what now??')
            print(K1)

    return R
