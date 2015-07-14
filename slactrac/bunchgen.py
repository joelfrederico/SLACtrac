import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
from .classes import *

__all__ = [
    'gaussbunch_sigmas',
    'gaussbunch_twiss'
    ]


def gaussbunch_sigmas(sx, sxp, sy, syp, sz, sd, n_parts):
    """
    Generates a gaussian bunch with RMS moments:

    * *sx*: RMS moment in :math:`x`
    * *sxp*: RMS moment in :math:`x'`
    * *sy*: RMS moment in :math:`y`
    * *syp*: RMS moment in :math:`y'`
    * *sz*: RMS moment in :math:`z'`
    * *sd*: RMS moment in :math:`\\delta = \\frac{p - p_0}{p_0}`

    Returns :class:`slactrac.Bunch`.
    """
    x  = _np.random.normal(loc=0, scale=sx, size=n_parts)
    xp = _np.random.normal(loc=0, scale=sxp, size=n_parts)

    y  = _np.random.normal(loc=0, scale=sy, size=n_parts)
    yp = _np.random.normal(loc=0, scale=syp, size=n_parts)

    z  = _np.random.normal(loc=0, scale=sz, size=n_parts)
    d  = _np.random.normal(loc=0, scale=sd, size=n_parts)

    return Bunch(x, xp, y, yp, z, d)


def gaussbunch_twiss(Beam_x, Beam_y, sz, sd, n_parts, szd=0):
    """
    Generates a gaussian bunch with:

    * *Beam_x*: :class:`slactrac.BeamParams` representation of beam properties in x
    * *Beam_y*: :class:`slactrac.BeamParams` representation of beam properties in y
    * *sz*: RMS moment in :math:`z'`
    * *sd*: RMS moment in :math:`\\delta = \\frac{p - p_0}{p_0}`

    Returns :class:`slactrac.Bunch`.
    """
    mean = _np.zeros(6)
    cov_xx = Beam_x.beta*Beam_x.emit
    cov_xxp = Beam_x.avg_xxp
    cov_xpxp = Beam_x.gamma*Beam_x.emit

    cov_yy = Beam_y.beta*Beam_y.emit
    cov_yyp = Beam_y.avg_xxp
    cov_ypyp = Beam_y.gamma*Beam_y.emit

    cov = _np.array(
        [
            [cov_xx   , cov_xxp   , 0        , 0         , 0                 , 0              ]    ,
            [cov_xxp  , cov_xpxp  , 0        , 0         , 0                 , 0              ]    ,
            [0        , 0         , cov_yy   , cov_yyp   , 0                 , 0              ]    ,
            [0        , 0         , cov_yyp  , cov_ypyp  , 0                 , 0              ]    ,
            [0        , 0         , 0        , 0         , _np.power(sz, 2)  , szd            ]    ,
            [0        , 0         , 0        , 0         , szd               , _np.power(sd, 2) ]
        ]
        )

    parts = _np.random.multivariate_normal(mean, cov, size=n_parts)
    x = parts[:, 0]
    xp = parts[:, 1]

    y = parts[:, 2]
    yp = parts[:, 3]

    z = parts[:, 4]
    d = parts[:, 5]

    return Bunch(x, xp, y, yp, z, d)
