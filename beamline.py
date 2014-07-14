# import scipy as _sp
import numpy as _np
from baseclass import baseclass
import copy as _copy
# from Twiss import Twiss as _Twiss
from BeamParams import BeamParams as _BeamParams
from conversions import gamma2GeV as _gamma2GeV

class Beamline(baseclass):
	_type    = 'beamline'
	_order   = int(1)
	def __init__(self,element_list,gamma,beam_x=None,beam_y=None):
		self._gamma   = _np.float64(gamma)
		# print len(element_list)
		# self.twiss_x = twiss_x
		# self.twiss_y = twiss_y
		self.beam_x = _copy.deepcopy(beam_x)
		self.beam_y = _copy.deepcopy(beam_y)
		self.elements = _np.array([])

		for element in element_list:
			self.elements = _np.append(self.elements,_copy.deepcopy(element))
		for element in self.elements:
			# element._gamma = self._gamma
			if ( element._order > self._order ):
				self._order = element._order

	# Define property length
	def _get_length(self):
		length = 0
		for element in self.elements:
			length += element._length
		return length
	length = property(_get_length,doc='The length of the beamline.')

	# Define transfer matrix R property
	def _getR(self):
		R = _np.identity(6)
		for i,element in enumerate(self.elements):
			R = _np.dot(element.R,R)
		return R
	R = property(_getR,doc='The transfer matrix R for the beamline.')

	# Define gamma property for beamlines
	# If you change gamma, it changes for all elements
	def _get_gamma(self):
		return self._gamma
	def _set_gamma(self,gamma):
		gamma = _np.float64(gamma)
		for element in self.elements:
			# Changes energy of element
			element.change_E(self._gamma,gamma)
		self._gamma = gamma
	gamma = property(_get_gamma,_set_gamma)

	def _get_beam_end(self,beam,slice_var):
		beamtemp = _copy.deepcopy(beam)
		R = _np.identity(6)
		print '========================================'
		for i,element in enumerate(self.elements):
			if element._type == 'scatter':
				beamtemp = beamtemp.transport(R[slice_var,slice_var])
				old_emit_n = beamtemp.emit*self.gamma
				theta_rms = element.theta_rms(_gamma2GeV(self.gamma))
				newdiv = _np.sqrt(beamtemp.divergence**2 + theta_rms**2)
				print 'Old divergence:\t\t{}\nAdded Divergence:\t{}\nNew Divergence:\t\t{}'.format(beamtemp.divergence,theta_rms,newdiv)
				beamtemp = _BeamParams(spotsize=beamtemp.spotsize,divergence=newdiv,avg_xxp=beamtemp.avg_xxp)
				new_emit_n = beamtemp.emit*self.gamma
				print 'Old emittance:\t\t{}\nNew emittance:\t\t{}'.format(old_emit_n,new_emit_n)
				print '-------------'
				R = _np.identity(6)
			else:
				R = _np.dot(element.R,R)

		out = beamtemp.transport(R[slice_var,slice_var])
		return out

	def _get_beam_x_end(self):
		slice_var = slice(0,2)
		out = self._get_beam_end(self.beam_x,slice_var)
		return out
	beam_x_end = property(_get_beam_x_end)

	def _get_beam_y_end(self):
		slice_var = slice(2,4)
		out = self._get_beam_end(self.beam_y,slice_var)
		return out
	beam_y_end = property(_get_beam_y_end)

	def _get_spotsize_x_end(self,emit=None,emit_n=None):
		return self.beam_x_end.spotsize
	spotsize_x_end = property(_get_spotsize_x_end)

	def _get_spotsize_y_end(self):
		return self.beam_y_end.spotsize
	spotsize_y_end = property(_get_spotsize_y_end)

	def writelattice(self,filename='out.lte'):
		f = open(filename,'w')
		string = 'C\t:CHARGE,TOTAL=3.2E-09'
		f.write(string + '\n')
		names = _np.array('C')

		# Write elements
		for i,obj in enumerate(self.elements):
			if obj._type == 'drift':
				name = 'CSRD{}'.format(i)
				names = _np.append(names,name)
				string = '{}\t:CSRDRIF,L={},USE_STUPAKOV=1,N_KICKS=1'.format(name,obj.length)
			elif obj._type == 'bend':
				name = 'BEND{}'.format(i)
				names = _np.append(names,name)
				string = ('{}\t:CSRCSBEN,L={}, &\n'
						'\t\tANGLE={}, &\n'
						'\t\tTILT={}, &\n'
						'\t\tN_KICKS=20, &\n'
						'\t\tSG_HALFWIDTH=1,&\n'
						'\t\tSG_ORDER=1,&\n'
						'\t\tSTEADY_STATE=0,&\n'
						'\t\tBINS=500').format(name,obj.length,obj.angle,obj.tilt)
			elif obj._type == 'quad':
				name = 'QUAD{}'.format(i)
				names = _np.append(names,name)
				string = '{}\t:QUAD,L={},K1={}'.format(name,obj.length,obj.K1)
			else:
				raise ValueError('Element not a drift, bend, or quad')
				
			f.write(string+'\n')

		# Write beamline
		string = '\nBEAMLINE\t:LINE('
		for i,val in enumerate(names):
			if i == 0:
				string = string + val
			else:
				string = string + ',' + val
		string = string + ')'

		f.write(string)

		f.close()
