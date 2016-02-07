class baseclass(object):
    """
    Defines a basic beamline element. All beamline elements should have a *length*, an *order*, and a *name* to identify them.
    """
    def __init__(self, length=0, order=1, name=None):
        self.ind     = None
        self._name    = name
        self._length = length
        self._order  = order
        self._type   = None
        self._ele_type = None

    def _not_allowed(self, *args, **kwargs):
        raise AttributeError('This attribute is not available for element type: {}'.format(self._type))

    K1        = property(_not_allowed, _not_allowed)
    angle     = property(_not_allowed, _not_allowed)
    rotate    = property(_not_allowed, _not_allowed)
    thickness = property(_not_allowed, _not_allowed)
    radlength = property(_not_allowed, _not_allowed)

    @property
    def _kwargs_str(self):
        string = ''
        for kname, kvalue in self._kwargs.items():
            string = string + ', {} = {}'.format(kname, kvalue)

        return string

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, namestr):
        self._name = namestr

    @property
    def order(self):
        return self._order
