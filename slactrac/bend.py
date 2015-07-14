import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np

from .driftmat import driftmat as _driftmat
from .baseclass import baseclass as _baseclass

__all__ = ['Bend']


class Bend(_baseclass):
    """
    Represents a bend with *length*, bend *angle*, rotation *rotate*, calculated to *order*, represented by *name*
    """
    def __init__(self, length=0, angle=0, order=1, rotate=0, name=None, **kwargs):
        self.name   = name
        self._type   = 'bend'
        self._length = _np.float_(length)
        self._order  = int(order)
        self._angle  = _np.float_(angle)
        self.rotate  = rotate
        self._kwargs = kwargs

    @property
    def rotate(self):
        """
        The orientation of the magnet.
        """
        return self._rotate

    @rotate.setter
    def rotate(self, val):
        self._rotate = val

    @property
    def R(self):
        """
        The first-order transfer matrix.
        """
        temp = bendmat(
            length = self._length,
            angle  = self._angle,
            order  = self._order
            )
        if self.rotate == 90:
            R          = _np.zeros([6, 6])
            R[0:2, 0:2] = temp[2:4, 2:4]
            R[2:4, 0:2] = temp[0:2, 2:4]
            R[0:2, 5]   = temp[2:4, 5]
            R[0:2, 2:4] = temp[2:4, 0:2]
            R[2:4, 2:4] = temp[0:2, 0:2]
            R[2:4, 5]   = temp[0:2, 5]
            R[4:6, 0:2] = temp[4:6, 2:4]
            R[4:6, 2:4] = temp[4:6, 0:2]
            R[4:6, 4:6] = temp[4:6, 4:6]
            # print('hi')
        elif self.rotate == 0:
            R = temp
        else:
            print('SERIOUS PROBLEM')
            R = temp
            # print('hi')
        return R

    @property
    def length(self):
        """
        The length of the magnet.
        """
        return self._length

    @property
    def angle(self):
        """
        The bend angle of the magnet in degrees.
        """
        return self._angle

    @property
    def tilt(self):
        """
        The bend angle of the magnet in radians.
        """
        return self.rotate*_np.pi/180

    def change_E(self, old_gamma, new_gamma):
        """
        Scale the setpoint energy of the magnet from the old energy *old_gamma* to new energy *new_gamma*.

        The best way to think about this is that the angle will change with different beam energy, so changing the beam energy changes the magnet's properties, because the magnet's B-field stays the same.
        """
        old_gamma = _np.float_(old_gamma)
        new_gamma = _np.float_(new_gamma)
        self._angle *= old_gamma / new_gamma

    @property
    def ele_name(self):
        """
        Returns the elegant-styled name.
        """
        name = 'BEND_{}_{:03.0f}'.format(self.name, self.ind)
        return name

    @property
    def ele_string(self):
        """
        Returns the full elegant entry.
        """
        string = (
            '{}\t:CSRCSBEN               , &\n'
            '\t\tL            = {:0.10e} , &\n'
            '\t\tANGLE        = {}       , &\n'
            '\t\tTILT         = {}       , &\n'
            '\t\tN_KICKS      = 20       , &\n'
            '\t\tSG_HALFWIDTH = 1        , &\n'
            '\t\tSG_ORDER     = 1        , &\n'
            '\t\tSTEADY_STATE = 0        , &\n'
            '\t\tBINS         = 500').format(self.ele_name, self.length, self.angle, self.tilt)
        string = string + self._kwargs_str

        return string


def bendmat(
        length=0,
        angle=0,
        order=1,
        fse=0,
        K1=0,
        K2=0
        ):

    if (( length == 0 ) or ( angle == 0 )):
        return _driftmat(length, order)

    # Make sure ints don't flow through
    length = _np.float_(length)
    angle  = _np.float_(angle)
    K1     = _np.float_(K1)
    K2     = _np.float_(K2)

    h     = angle/length            # /* coordinate system curvature */
    ha    = h*(1+fse)               # /* actual curvature due to bending field */
    n     = -K1/_np.square(h)              # /* field index */
    beta  = K2/2/pow(h, 3)            # /* sextupole index */
    gamma = 0

    t0      = length
    nh      = n*h
    betah2  = beta*_np.square(h)  # noqa
    gammah3 = gamma*pow(h, 3)  # noqa
    
    # M = sbend_matrix(length, h, ha, n*h, beta*sqr(h), gamma*pow3(h), order)
    h2 = h*h
    ha2 = ha*ha  # noqa

    kx2 = -(h2 - 2*h*ha + nh*ha)
    ky2 = nh*ha
    ky2_is_zero = (ky2 == 0)  # noqa
    kx2_is_zero = (kx2 == 0)  # noqa

    small3 = pow(1e-16, 1./3.)

    if (_np.sqrt(abs(kx2))*t0 < small3):
        kx2 = _np.square(small3/t0)
        if (kx2):
            kx2 = _np.sign(kx2)*kx2

    if (kx2 > 0.0):
            kx = _np.sqrt(kx2)
            cx = _np.cos(kx*t0)
            sx = _np.sin(kx*t0)/kx
    elif (kx2 < 0.0):
            kx = _np.sqrt(-kx2)
            cx = _np.cosh(kx*t0)
            sx = _np.sinh(kx*t0)/kx

    if (abs(ky2) < small3):
        ky2 = _np.square(small3/t0)
        if (ky2):
            ky2 = _np.sign(ky2)*ky2

    if (ky2 > 0.0):
            ky = _np.sqrt(ky2)
            cy = _np.cos(ky*t0)
            sy = _np.sin(ky*t0)/ky
    elif (ky2 < 0.0):
            ky = _np.sqrt(-ky2)
            cy = _np.cosh(ky*t0)
            sy = _np.sinh(ky*t0)/ky

    R = _np.identity(6)
    if (h != 0):
        R[0][0] = R[1][1] = cx
        R[0][1] = sx
        R[0][2] = R[0][3] = R[0][4] = 0
        R[0][5] = -ha*(cx-1)/kx2
        R[1][0] = -sx*kx2
        R[1][2] = R[1][3] = R[1][4] = 0
        R[1][5] = sx*ha
        R[2][2] = R[3][3] = cy
        R[2][3] = sy
        R[2][0] = R[2][1] = R[2][4] = R[2][5] = 0
        R[3][2] = - sy*ky2
        R[3][0] = R[3][1] = R[3][4] = R[3][5] = 0
        R[4][0] = h*sx
        R[4][1] = -(h*(cx - 1))/kx2
        R[4][2] = R[4][3] = 0
        R[4][5] = (h*ha*(t0 - sx))/kx2
    else:
        # /* steering corrector */
        R[0][0] = R[1][1] = R[2][2] = R[3][3] = 1
        R[0][1] = R[2][3] = t0
        R[0][5] = C[0] + t0*_np.sin(ha*t0)  # noqa
        R[1][5] = t0*ha*_np.cos(ha*t0)

    R[5][0] = R[5][1] = R[5][2] = R[5][3] = R[5][4] = 0
    R[4][4] = R[5][5] = 1
 
    return R
