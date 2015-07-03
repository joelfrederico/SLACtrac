import numpy as np
from .classes import *

__all__ = ['gaussbunch_twiss']


def gaussbunch_sigmas(sx, sxp, sy, syp, sz, sd, n_parts):
    x  = np.random.normal(loc=0, scale=sx, size=n_parts)
    xp = np.random.normal(loc=0, scale=sxp, size=n_parts)

    y  = np.random.normal(loc=0, scale=sy, size=n_parts)
    yp = np.random.normal(loc=0, scale=syp, size=n_parts)

    z  = np.random.normal(loc=0, scale=sz, size=n_parts)
    d  = np.random.normal(loc=0, scale=sd, size=n_parts)

    return Bunch(x, xp, y, yp, z, d)


def gaussbunch_twiss(Beam_x, Beam_y, sz, sd, n_parts, szd=0):
    mean = np.zeros(6)
    cov_xx = Beam_x.beta*Beam_x.emit
    cov_xxp = Beam_x.avg_xxp
    cov_xpxp = Beam_x.gamma*Beam_x.emit

    cov_yy = Beam_y.beta*Beam_y.emit
    cov_yyp = Beam_y.avg_xxp
    cov_ypyp = Beam_y.gamma*Beam_y.emit

    cov = np.array(
            [
                [cov_xx  ,  cov_xxp  ,  0       ,  0        ,  0              ,  0              ] ,
                [cov_xxp ,  cov_xpxp ,  0       ,  0        ,  0              ,  0              ] ,
                [0       ,  0        ,  cov_yy  ,  cov_yyp  ,  0              ,  0              ] ,
                [0       ,  0        ,  cov_yyp ,  cov_ypyp ,  0              ,  0              ] ,
                [0       ,  0        ,  0       ,  0        ,  np.power(sz, 2) ,  szd            ] ,
                [0       ,  0        ,  0       ,  0        ,  szd            ,  np.power(sd, 2) ]
            ]
        )

    parts = np.random.multivariate_normal(mean, cov, size=n_parts)
    x = parts[:, 0]
    xp = parts[:, 1]

    y = parts[:, 2]
    yp = parts[:, 3]

    z = parts[:, 4]
    d = parts[:, 5]

    return Bunch(x, xp, y, yp, z, d)
