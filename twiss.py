import numpy as _np

class Twiss(object):
	def __init__(self,beta,alpha):
		self.beta=beta
		self.alpha=alpha

	# Definte beta property
	# Validate beta > 0
	def _set_beta(self,value):
		if not (value > 0):
			raise ValueError('Beta must be greater than zero: requested beta={}.'.format(value))
		self._beta=value
	def _get_beta(self):
		return self._beta
	beta = property(_get_beta,_set_beta)
	
	# Define gamma property
	# Derived from beta and alpha
	def _get_gamma(self):
		return (1+_np.power(self.alpha,2))/self.beta
	gamma=property(_get_gamma)

	# Define T matrix
	# Derived from beta, alpha, and gamma
	def _get_T(self):
		return _np.array([[self.beta,-self.alpha],[-self.alpha,self.gamma]])
	T=property(_get_T)

	# Define transport method
	# Returns new twiss given R matrix.
	def transport(self,R):
		T2 = _np.dot(_np.dot(R,self.T),_np.transpose(R))
		betaf = T2[0,0]
		alphaf = -T2[0,1]
		return Twiss(betaf,alphaf)

	# Define spotsize method
	# Returns spot size given an emittance
	def spotsize(self,emit):
		return _np.sqrt(self.beta*emit)
