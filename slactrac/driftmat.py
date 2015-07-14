import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
from .baseclass import baseclass as _baseclass

__all__ = ['Drift']


class Drift(_baseclass):
    """
    Represents a drift with *length* calculated to *order* to use the *name* to identify it.
    """
    def __init__(self, length=0, order=1, name=None, **kwargs):
        self.name   = name
        self._type   = 'drift'
        self._length = _np.float64(length)
        self._order  = int(order)
        self._kwargs = kwargs

    # Define transfer matrix property R
    @property
    def R(self):
        """
        The first-order transfer matrix.
        """
        return driftmat(self._length, self._order)

    def change_E(self, old_gamma, new_gamma):
        """
        Scale the energy of the drift. (Does nothing in a drift.)
        """
        pass

    @property
    def length(self, verbose=False):
        """
        The length of the drift.
        """
        if verbose:
            print('This is a drift matrix')
        return self._length

    @length.setter
    def length(self, value):
        print('Length changing for element ({}) from {} to {}'.format(self.name, self._length, value))
        self._length = _np.float64(value)

    @property
    def ele_name(self):
        """
        Returns the elegant-styled name.
        """
        name = 'CSRD_{}_{:03.0f}'.format(self.name, self.ind)
        return name

    @property
    def ele_string(self):
        """
        Returns the full elegant entry.
        """
        string = '{}\t:CSRDRIF,L={},USE_STUPAKOV=1,N_KICKS=1'.format(self.ele_name, self.length)
        string = string + self._kwargs_str

        return string


def driftmat(l=0, order=1):
    R_small = _np.array(
        [[ 1 , l ],
        [  0 , 1 ]]
        )
    R_small = _np.float_(R_small)

    R = _np.zeros([6, 6])
    R[0:2, 0:2] = R[2:4, 2:4] = R_small
    R[4:6, 4:6] = _np.float_(_np.identity(2))
    return R
