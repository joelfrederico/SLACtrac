class baseclass(object):
	def __init__(self,length=0,order=1,name=None):
		self.name    = name
		self._length = length
		self._order  = order
		self._type   = None

	def _not_allowed(self,*args,**kwargs):
		raise AttributeError('This attribute is not available for element type: {}'.format(self._type))

	K1        = property(_not_allowed,_not_allowed)
	angle     = property(_not_allowed,_not_allowed)
	rotate    = property(_not_allowed,_not_allowed)
	thickness = property(_not_allowed,_not_allowed)
	radlength = property(_not_allowed,_not_allowed)
