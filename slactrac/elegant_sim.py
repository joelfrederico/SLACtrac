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

def elegant_sim(beamline,dir=None,filename=None,**kwargs):
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
    if filename is None:
        fd,filename = tempfile.mkstemp(dir=path,prefix='out_',suffix='.ele')
        f = os.fdopen(fd,'w+')
    else:
        f = open(os.path.join(path,filename),'w+')
    logger.log(level=loggerlevel,msg='Filename is: {}'.format(filename))

    basename = os.path.basename(filename)
    root,ext = os.path.splitext(basename)
    lte_name = os.path.join(path,'{}.lte'.format(root))
    beamline.elegant_lte(filename=lte_name)
    
    # ======================================
    # Get template path from package and
    # load template
    # ======================================
    templates_path = pkg_resources.resource_filename(__name__,'templates')
    loader = jj.FileSystemLoader(templates_path)
    env = jj.Environment(loader=loader)
    template = env.get_template('template.ele')
    
    # ======================================
    # Generate ele file
    # ======================================
    template.stream(filename=lte_name,matched=0,**kwargs).dump(f)
    f.close()

    # ======================================
    # Run Elegant
    # ======================================
    command = 'elegant {}'.format(filename)
    logger.log(level=loggerlevel,msg='Command is: {}'.format(command))

    log_name = os.path.join(path,'{}.log'.format(root))
    f_log = open(log_name,'w+')
    logger.log(level=loggerlevel,msg='Log file is: {}'.format(log_name))

    #  fnull = open(os.devnull,'w')
    cwdu = os.getcwdu()
    os.chdir(path)
    subprocess.call(shlex.split(command),stdout=f_log,stderr=f_log)
    os.chdir(cwdu)

    # ======================================
    # Clean temporary directory if necessary
    # ======================================
    if dir is None:
        shutil.rmtree(path)

    return path,root,ext
