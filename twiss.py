import numpy as _np

class Twiss(object):
	def __repr__(self):
		return '<{} at {}; beta={}, alpha={}>'.format(self.__class__.__module__,hex(id(self)),self.beta,self.alpha)

	def __init__(self,beta,alpha):
		self.beta=_np.float64(beta)
		self.alpha=_np.float64(alpha)

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
	def spotsize(self,emit=None,emit_n=None,gamma=None):
		# if emit==None and emit_n==None:
		# 	raise ValueError('Did not specify an emittance!')
		# if emit!=None and emit_n!=None:
		# 	raise ValueError('Specified too many emittance values!')
		# if emit_n!=None:
		# 	# print emit_n
		# 	emit = emit_n/gamma
		return _np.sqrt(self.beta*emit)
