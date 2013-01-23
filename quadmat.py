import scipy as sp
import numpy as np

def quadmat(k=0,l=0,order=1):
	if ( k == 0 ):
		R = drift(l,order)
	else if ( k > 0 ):
		kl = np.sqrt(k) * l
		sin_kl = np.sin(kl)
		cos_kl = np.cos(kl)
		R = np.array(
				[[ cos_kl    , sin_kl/k ],
				[  -k*sin_kl , cos_kl   ]]
			)
	return R
