import ipdb
import jinja2 as jj
import logging
import os
import pkg_resources
import shlex
import shutil
import tempfile
import subprocess

logger=logging.getLogger(__name__)
loggerlevel = logging.DEBUG
#  loggerlevel = 9

__all__ = ['elegant_sim']

def elegant_sim(beamline,dir=None):
    # ======================================
    # If path isn't specified, create
    # temporary one
    # ======================================
    if dir is None:
        path = tempfile.mkdtemp()
        logger.log(level=loggerlevel,msg='Path is: {}'.format(path))
    else:
        path = dir

    # ======================================
    # Open up a temporary file in the path
    # ======================================
    fd,filename = tempfile.mkstemp(dir=path,prefix='out_',suffix='.ele')
    f = os.fdopen(fd,'w+')
    logger.log(level=loggerlevel,msg='Filename is: {}'.format(filename))

    basename = os.path.basename(filename)
    lte_name = '{}.lte'.format(basename)
    beamline.elegant_lte(filename=lte_name)
    
    templates_path = pkg_resources.resource_filename(__name__,'templates')
    ipdb.set_trace()
    loader = jj.FileSystemLoader(templates_path)
    env = jj.Environment(loader=loader)
    
    template = env.get_template('template.ele')
    
    template.stream(filename=lte_name,matched=0).dump(f)

    command = 'elegant {}'.format(filename)
    logger.log(level=loggerlevel,msg='Command is: {}'.format(command))
    
    subprocess.call(shlex.split(command))

    if dir is None:
        shutil.rmtree(path)
