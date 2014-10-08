import numpy as _np

class BeamParams(object):
	def __repr__(self):
		return '<{} at {}; beta={}, alpha={}>'.format(self.__class__.__module__,hex(id(self)),self.beta,self.alpha)

	def __init__(self,
			beta=None,alpha=None,emit=None,emit_n=None,gamma=None,
			spotsize=None,divergence=None,r=None,avg_xxp=None):
		# If not enough info for Twiss
		emit_norm_insufficient = (emit_n==None or gamma==None)
		emit_geom_insufficient = emit==None
		emit_insufficient = (emit_geom_insufficient and emit_norm_insufficient)
		shape_insufficient = (beta==None or alpha==None)
		twiss_insufficient = (shape_insufficient or emit_insufficient)
		moments_insufficient = (spotsize==None or divergence==None or (r==None and avg_xxp==None))

		# Validation that there's enough info to construct everything
		if twiss_insufficient and moments_insufficient:
			raise ValueError('Not enough information to construct Twiss values')

		if twiss_insufficient:
			if avg_xxp!=None:
				emit = _np.sqrt(spotsize**2 * divergence**2 - avg_xxp**2)
				corr_sign = _np.sign(avg_xxp)
			elif r!=None:
				emit = spotsize * divergence * _np.sqrt(1-r**2)
				corr_sign = _np.sign(r)
			else:
				raise ValueError('Missing avg_xxp/r term')
			beta = spotsize**2/emit
			gamma = divergence**2/emit
			alpha = -corr_sign * _np.sqrt(gamma*beta-1)
		else:
			def _get_geom_emit(emit=None,emit_n=None,gamma=None):
				if emit==None and emit_n==None:
					raise ValueError('Did not specify an emittance!')
				if emit!=None and emit_n!=None:
					raise ValueError('Specified too many emittance values!')
				if emit_n!=None:
					# print emit_n
					emit = _np.float64(emit_n)/_np.float64(gamma)
				else:
					emit = _np.float64(emit)
				return emit
			emit=_get_geom_emit(emit=emit,emit_n=emit_n,gamma=gamma)

		self.beta=_np.float64(beta)
		self.alpha=_np.float64(alpha)
		self.emit=_np.float64(emit)

	def set_emit_n(self,emit_n,gamma):
		self.emit=_np.float64(emit_n/gamma)


	# Definte beta property
	# Validate beta > 0
	def _get_beta(self):
		return self._beta
	def _set_beta(self,value):
		if not (value > 0):
			raise ValueError('Beta must be greater than zero: requested beta={}.'.format(value))
		self._beta=value
	beta = property(_get_beta,_set_beta)
	
	def _get_betastar(self):
		return 1/self.gamma
	betastar=property(_get_betastar)

	def _get_sstar(self):
		return self.alpha/self.gamma
	sstar=property(_get_sstar)

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
		return BeamParams(beta=betaf,alpha=alphaf,emit=self.emit)

	# Define spotsize method
	def _get_spotsize(self):
		return _np.sqrt(self.beta*self.emit)
	spotsize=property(_get_spotsize)

	def _get_divergence(self):
		return _np.sqrt(self.gamma*self.emit)
	def _set_divergence(self,value):
		self.emit = value**2/self.gamma
		# print self.divergence
		# print self.emit
	divergence=property(_get_divergence,_set_divergence)

	def _get_avg_xxp(self):
		 return -self.alpha*self.emit
	avg_xxp = property(_get_avg_xxp)

	def _get_minspotsize(self):
		return _np.sqrt(self.betastar*self.emit)
	minspotsize = property(_get_minspotsize)
