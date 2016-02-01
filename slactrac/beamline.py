import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
from .beamparams import BeamParams as _BeamParams
from .baseclass import baseclass as _baseclass
from .conversions import gamma2GeV as _gamma2GeV
import copy as _copy
import logging as _logging
import warnings as _warnings

_logger = _logging.getLogger(__name__)
#  _loggerlevel = _logging.DEBUG
_loggerlevel = 9

#  class Elements(object):
#      def __init__(self, element_list, verbose=None):
#          self._elements


class Beamline(_baseclass):
    """
    Represents a beamline composed of various elements.

    Parameters
    ----------

    element_list : float
        A list of all the elements in order in the beamline.
    gamma : float
        The beamline energy.
    beam_x : float
        :class:`slactrac.Beamparams` class representing the x coordinates.
    beam_y : float
        :class:`slactrac.Beamparams` class representing the y coordinates.
    verbose : float
        If true, prints details of beam setup on the terminal.
    """
    _type    = 'beamline'
    _order   = int(1)

    def __init__(self, element_list, gamma, beam_x=None, beam_y=None, verbose=False):
        self.verbose = verbose
        self._gamma   = _np.float64(gamma)
        self.beam_x   = _copy.deepcopy(beam_x)
        self.beam_y   = _copy.deepcopy(beam_y)
        self.elements = _np.array([])

        for element in element_list:
            self.elements = _np.append(self.elements, _copy.deepcopy(element))
        for i, element in enumerate(self.elements):
            # element._gamma = self._gamma
            if (element._order > self._order):
                self._order = element._order
            if element.name is None:
                _warnings.warn('Missing name for {}-th element of beamline element list'.format(i), SyntaxWarning, stacklevel=2)
            element.ind = i

    def change_verbose(self, verbose=False):
        """
        Change whether the beamline is verbose.
        """
        for i, element in enumerate(self.elements):
            self.elements[i].verbose = verbose

    # Define property length
    @property
    def length(self):
        """
        The length of the beamline.
        """
        length = 0
        for element in self.elements:
            length += element._length
        return length

    # Define transfer matrix R property
    @property
    def R(self):
        """
        The transfer matrix R for the beamline.
        """
        R = _np.identity(6)
        for i, element in enumerate(self.elements):
            R = _np.dot(element.R, R)
        return R

    # Define gamma property for beamlines
    # If you change gamma, it changes for all elements
    @property
    def gamma(self):
        """
        The energy setpoint of the beamline.
        """
        return self._gamma

    @gamma.setter
    def gamma(self, gamma):
        gamma = _np.float64(gamma)
        for element in self.elements:
            # Changes energy of element
            element.change_E(self._gamma, gamma)
        self._gamma = gamma

    def _get_beam_end(self, beam, slice_var):
        beamtemp = _copy.deepcopy(beam)
        R = _np.identity(6)
        for i, element in enumerate(self.elements):
            if element._type == 'scatter':
                if self.verbose & element.verbose:
                    beamtemp   = beamtemp.transport(R[slice_var, slice_var])
                    old_emit_n = beamtemp.emit*self.gamma
                    theta_rms  = element.theta_rms(_gamma2GeV(self.gamma))
                    newdiv     = _np.sqrt(beamtemp.divergence**2 + theta_rms**2)
                    print('\t------------------------------------------------')
                    print('\tScatter element')
                    print('\tElement name: {}'.format(element.name))
                    print('\tDivergence:\n\t\tOld divergence:\t\t{:.3e}\n\t\tAdded Divergence:\t{:.3e}\n\t\tNew Divergence:\t\t{:.3e}\n\t\tFraction change:\t{:.3e}'.format(beamtemp.divergence, theta_rms, newdiv, newdiv/beamtemp.divergence-1))
                    beamtemp   = _BeamParams(spotsize=beamtemp.spotsize, divergence=newdiv, avg_xxp=beamtemp.avg_xxp)
                    new_emit_n = beamtemp.emit*self.gamma
                    print('\tEmittance:\n\t\tOld emittance:\t\t{}\n\t\tNew emittance:\t\t{}\n\t\tFraction change:\t{:.3e}'.format(old_emit_n, new_emit_n, new_emit_n/old_emit_n-1))
                    print('\t------------------------------------------------')
                    R = _np.identity(6)
            else:
                R = _np.dot(element.R, R)

        out = beamtemp.transport(R[slice_var, slice_var])
        return out

    @property
    def beam_x_end(self):
        """
        The beam parameters in x at the end of the beamline.
        """
        slice_var = slice(0, 2)
        out = self._get_beam_end(self.beam_x, slice_var)
        return out

    @property
    def beam_y_end(self):
        """
        The beam parameters in y at the end of the beamline.
        """
        slice_var = slice(2, 4)
        out = self._get_beam_end(self.beam_y, slice_var)
        return out

    @property
    def spotsize_x_end(self, emit=None, emit_n=None):
        """
        The beam spotsize in x at the end of the beamline.
        """
        return self.beam_x_end.spotsize

    @property
    def spotsize_y_end(self):
        """
        The beam spotsize in x at the end of the beamline.
        """
        if self.verbose:
            print('================================================')
            print('Verbose Beamline Printing in _get_spotsize_y_end...')
            print('================================================')
            print('Starting norm. emittance: {}'.format(self.beam_y.emit*self.gamma))
            print('Starting spot in y: {}'.format(self.beam_y.spotsize))
            print('Starting emittance: {}'.format(self.beam_y.emit))
            print('Starting beta: {}'.format(self.beam_y.beta))
        out = self.beam_y_end.spotsize
        if self.verbose:
            print('\t------------------------------------------------')
            print('\tFinal spot size: {:.3f} mm'.format(out*1e3))
            print('\t------------------------------------------------')
        return out

    def elegant_lte(self, filename='out.lte', scatter_enable=False):
        """
        Writes the beamline to an Elegant lte lattice file with *filename*.

        * *scatter_enable*: Determines if scatter elements are used.
        """
        f = open(filename, 'w')
        string = 'C\t:CHARGE,TOTAL=3.2E-09'
        f.write(string + '\n')
        names = _np.array('C')

        # Write elements
        for i, obj in enumerate(self.elements):
            if obj._type == 'scatter':
                if scatter_enable:
                    string = obj.ele_string(i, self.gamma)
                    names = _np.append(names, obj.ele_name)
                else:
                    continue
            else:
                string = obj.ele_string
                names = _np.append(names, obj.ele_name)

            _logger.log(level=_loggerlevel, msg='Name is: {}'.format(obj.ele_name))
            _logger.log(level=_loggerlevel, msg='Iteration is: {}'.format(i))
            f.write(string+'\n\n')

        # Write beamline
        string = '\nBEAMLINE\t:LINE=(&\n'
        for i, val in enumerate(names):
            if i == 0:
                string = string + '\t\t\t' + val
            else:
                string = string + ', &' + '\n\t\t\t' + val
        string = string + '  &\n\t\t\t)'

        f.write(string)

        f.close()
