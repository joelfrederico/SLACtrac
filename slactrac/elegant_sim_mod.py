import jinja2 as _jj
import os as _os
import pkg_resources as _pkg_resources
import shlex as _shlex
import shutil as _shutil
import tempfile as _tempfile
import subprocess as _subprocess

import logging as _logging
_logger      = _logging.getLogger(__name__)
_loggerlevel = _logging.DEBUG
#  _loggerlevel = 9

__all__ = ['elegant_sim']


def elegant_sim(beamline, dir=None, filename=None, **kwargs):
    """
    Creates and runs a simulation in Elegant.


    Parameters
    ----------

    dir : str
        If none, simulated in a :func:`tempfile.mkdtemp` temporary directory.
    filename : str
        If none, simulated with a :func:`tempfile.mkstemp` temporary file.

    Returns
    -------

    (path, root, ext) : (str, str, str)
        A tuple of the path of the simulation, the filename of the simulation, and the extension of the simulation
    """
    # ======================================
    # If path isn't specified, create
    # temporary one
    # ======================================
    if dir is None:
        path = _tempfile.mkdtemp()
        _logger.log(level=_loggerlevel, msg='Path is: {}'.format(path))
    else:
        path = dir

    # ======================================
    # Open up a temporary file in the path
    # ======================================
    if filename is None:
        fd, filename = _tempfile.mkstemp(dir=path, prefix='out_', suffix='.ele')
        f = _os.fdopen(fd, 'w+')
    else:
        f = open(_os.path.join(path, filename), 'w+')
    _logger.log(level=_loggerlevel, msg='Filename is: {}'.format(filename))

    basename = _os.path.basename(filename)
    root, ext = _os.path.splitext(basename)
    lte_name = _os.path.join(path, '{}.lte'.format(root))
    beamline.elegant_lte(filename=lte_name)
    
    # ======================================
    # Get template path from package and
    # load template
    # ======================================
    templates_path = _pkg_resources.resource_filename(__name__, 'templates')
    loader = _jj.FileSystemLoader(templates_path)
    env = _jj.Environment(loader=loader)
    template = env.get_template('template.ele')
    
    # ======================================
    # Generate ele file
    # ======================================
    template.stream(filename=lte_name, matched=0, **kwargs).dump(f)
    f.close()

    # ======================================
    # Run Elegant
    # ======================================
    command = 'elegant {}'.format(filename)
    _logger.log(level=_loggerlevel, msg='Command is: {}'.format(command))

    log_name = _os.path.join(path, '{}.log'.format(root))
    f_log = open(log_name, 'w+')
    _logger.log(level=_loggerlevel, msg='Log file is: {}'.format(log_name))

    #  fnull = open(_os.devnull, 'w')
    cwdu = _os.getcwdu()
    _os.chdir(path)
    _subprocess.call(_shlex.split(command), stdout=f_log, stderr=f_log)
    _os.chdir(cwdu)

    # ======================================
    # Clean temporary directory if necessary
    # ======================================
    if dir is None:
        _shutil.rmtree(path)

    return path, root, ext
