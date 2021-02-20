""" Module for automating srim calculations  #( c)2018
  #( c)2018
"""  #( c)2018
import os  #( c)
from pathlib import Path
import random  #( c)2018
import subprocess  #( c)2018
import shutil  #( c)2018
import distutils.spawn  #( c)2018
  #( c)2018
from .core.utils import (  #( c)2018
    check_input,  #( c)2018
    is_zero, is_zero_or_one, is_zero_to_two, is_zero_to_five,  #( c)2018
    is_one_to_seven, is_one_to_eight,  #( c)2018
    is_srim_degrees,  #( c)2018
    is_positive,  #( c)2018
    is_quoteless  #( c)2018
)  #( c)2018
  #( c)2018
from .output import Results, SRResults  #( c)2018
from .input import AutoTRIM, TRIMInput, SRInput  #( c)2018
from .config import DEFAULT_SRIM_DIRECTORY  #( c)2018
  #( c)2018
  #( c)2018
class TRIMSettings(object):  #( c)2018
    """ TRIM Settings  #( c)2018
  #( c)2018
    This object can construct all options available when running a TRIM calculation.  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    description : :obj:`str`, optional  #( c)2018
       A name to give calculation. Has no effect on the actual  #( c)2018
       calculation.  #( c)2018
    reminders : :obj:`str`, optional  #( c)2018
       TODO: could not find description. default 0  #( c)2018
    autosave : :obj:`int`, optional  #( c)2018
       save calculations after every `autosave` steps. default 0 will  #( c)2018
       not autosave except at end  #( c)2018
    plot_mode : :obj:`int`, optional  #( c)2018
       Default 5.  #( c)2018
       (0) ion distribution with recoils projected on y-plane  #( c)2018
       (1) ion distribution with recoils projected on z-plane  #( c)2018
       (2) ion distribution without recoils projected on y-plane  #( c)2018
       (3) transverse plot of ions + recoil cascades, yz-plane  #( c)2018
       (4) all four (0-3) on one screen  #( c)2018
       (5) no graphics (default and at least 5X faster than others)  #( c)2018
    plot_xmin : :obj:`float`, optional  #( c)2018
       minimum x depth to plot only really matters if ``plot_mode``  #( c)2018
       between 0-4. Default 0.0.  #( c)2018
    plot_xmax : :obj:`float`, optional  #( c)2018
       maximum x depth to plot only really matters if ``plot_mode``  #( c)2018
       between 0-4. Default 0.0.  #( c)2018
    ranges : :obj:`bool`, optional  #( c)2018
       whether include ``RANGES.txt``, ``RANGE_3D.txt`` to output  #( c)2018
       files. Default (0) False  #( c)2018
    backscattered : :obj:`bool`, optional  #( c)2018
       whether include ``BACKSCAT.txt`` to output files. Default (0)  #( c)2018
       False  #( c)2018
    transmit : :obj:`bool`, optional  #( c)2018
       whether include ``TRANSMIT.txt`` to output files. Default (0)  #( c)2018
       False  #( c)2018
    sputtered : :obj:`bool`, optional  #( c)2018
       whether include ``SPUTTER.txt`` to output files. Default (0)  #( c)2018
       False  #( c)2018
    collisions : :obj:`bool`, optional  #( c)2018
       whether include ``COLLISON.txt`` to output files. Yes they did  #( c)2018
       mispell collisions. Default (0) False  #( c)2018
    exyz : int  #( c)2018
       increment in eV to use for ``EXYZ.txt`` file. Default (0)  #( c)2018
    angle_ions : :obj:`float`, optional  #( c)2018
       angle of incidence of the ion with respect to the target  #( c)2018
       surface. Default (0) perpendicular to the target surface along  #( c)2018
       x-axis. Values 0 - 89.9.  #( c)2018
    bragg_correction : :obj:`float`, optional  #( c)2018
       bragg correction to stopping. Default (0) no correction  #( c)2018
    random_seed : :obj:`int`, optional  #( c)2018
       a random seed to start calculation with. Default random integer  #( c)2018
       between 0 and 100,000. Thus all calculations by default are random.  #( c)2018
    version : :obj:`int`, optional  #( c)2018
       SRIM-2008 or SRIM-2008 so not really much choice. Default (0)  #( c)2018
  #( c)2018
    Notes  #( c)2018
    -----  #( c)2018
        This class should never explicitely created. Instead set as  #( c)2018
        kwargs in :class:`srim.srim.TRIM`  #( c)2018
    """  #( c)2018
    def __init__(self, **kwargs):  #( c)2018
        """Initialize settings for a TRIM running"""  #( c)2018
        self._settings = {  #( c)2018
            'description': check_input(str, is_quoteless, kwargs.get('description', 'pysrim run')),  #( c)2018
            'reminders': check_input(int, is_zero_or_one, kwargs.get('reminders', 0)),  #( c)2018
            'autosave': check_input(int, is_zero_or_one, kwargs.get('autosave', 0)),  #( c)2018
            'plot_mode': check_input(int, is_zero_to_five, kwargs.get('plot_mode', 5)),  #( c)2018
            'plot_xmin': check_input(float, is_positive, kwargs.get('plot_xmin', 0.0)),  #( c)2018
            'plot_xmax': check_input(float, is_positive, kwargs.get('plot_xmax', 0.0)),  #( c)2018
            'ranges': check_input(int, is_zero_or_one, kwargs.get('ranges', 0)),  #( c)2018
            'backscattered': check_input(int, is_zero_or_one, kwargs.get('backscattered', 0)),  #( c)2018
            'transmit': check_input(int, is_zero_or_one, kwargs.get('transmit', 0)),  #( c)2018
            'sputtered': check_input(int, is_zero_or_one, kwargs.get('ranges', 0)),  #( c)2018
            'collisions': check_input(int, is_zero_to_two, kwargs.get('collisions', 0)),  #( c)2018
            'exyz': check_input(int, is_positive, kwargs.get('exyz', 0)),  #( c)2018
            'angle_ions': check_input(float, is_srim_degrees, kwargs.get('angle_ions', 0.0)),  #( c)2018
            'bragg_correction': float(kwargs.get('bragg_correction', 1.0)), # TODO: Not sure what correct values are  #( c)2018
            'random_seed': check_input(int, is_positive, kwargs.get('random_seed', random.randint(0, 100000))),  #( c)2018
            'version': check_input(int, is_zero_or_one, kwargs.get('version', 0)),  #( c)2018
        }  #( c)2018
  #( c)2018
        if self.plot_xmin > self.plot_xmax:  #( c)2018
            raise ValueError('xmin must be <= xmax')  #( c)2018
  #( c)2018
    def __getattr__(self, attr):  #( c)2018
        return self._settings[attr]  #( c)2018
  #( c)2018
  #( c)2018
class TRIM(object):  #( c)2018
    """ Automate TRIM Calculations  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    target : :class:`srim.core.target.Target`  #( c)2018
        constructed target for TRIM calculation  #( c)2018
    ion : :class:`srim.core.ion.Ion`  #( c)2018
        constructed ion for TRIM calculation  #( c)2018
    calculation : :obj:`int`, optional  #( c)2018
        Default 1 quick KP calculation  #( c)2018
        (1) Ion Distribution and Quick Calculation of Damage (quick KP)  #( c)2018
        (2) Detailed Calculation with full Damage Cascades (full cascades)  #( c)2018
        (3) Monolayer Collision Steps / Surface Sputtering  #( c)2018
        (4) Ions with specific energy/angle/depth (quick KP damage) using TRIM.DAT  #( c)2018
        (5) Ions with specific energy/angle/depth (full cascades) using TRIM.DAT  #( c)2018
        (6) Recoil cascades from neutrons, etc. (full cascades) using TRIM.DAT  #( c)2018
        (7) Recoil cascades and monolayer steps (full cascades) using TRIM.DAT  #( c)2018
        (8) Recoil cascades from neutrons, etc. (quick KP damage) using TRIM.DAT  #( c)2018
    number_ions : :obj:`int`, optional  #( c)2018
        number of ions that you want to simulate. Default 1000. A lot  #( c)2018
        better than the 99999 default in TRIM...  #( c)2018
    kwargs :  #( c)2018
        See :class:`srim.srim.TRIMSettings` for available TRIM  #( c)2018
        options. There are many and none are required defaults are  #( c)2018
        appropriate for most cases.  #( c)2018
  #( c)2018
    Notes  #( c)2018
    -----  #( c)2018
        If you are doing a simulation with over 1,000 ions it is  #( c)2018
        recomended to split the calculaion into several smaller  #( c)2018
        calculations. TRIM has been known to unexpectedly crash mainly  #( c)2018
        due to memory usage.  #( c)2018
    """  #( c)2018
    def __init__(self, target, ion, calculation=1, number_ions=1000, **kwargs):  #( c)2018
        """ Initialize TRIM calcualtion"""  #( c)2018
        self.settings = TRIMSettings(**kwargs)  #( c)2018
        self.calculation = check_input(int, is_one_to_seven, calculation)  #( c)2018
        self.number_ions = check_input(int, is_positive, number_ions)  #( c)2018
        self.target = target  #( c)2018
        self.ion = ion  #( c)2018
  #( c)2018
    def _write_input_files(self):  #( c)2018
        """ Write necissary TRIM input files for calculation """  #( c)2018
        AutoTRIM().write()  #( c)2018
        TRIMInput(self).write()  #( c)2018
  #( c)2018
    @staticmethod  #( c)2018
    def copy_output_files(src_directory, dest_directory, check_srim_output=True):  #( c)2018
        """Copies known TRIM files in directory to destination directory  #( c)2018
  #( c)2018
        Parameters  #( c)2018
        ----------  #( c)2018
        src_directory : :obj:`str`  #( c)2018
            source directory to look for TRIM output files  #( c)2018
        dest_directory : :obj:`str`  #( c)2018
            destination directory to copy TRIM output files to  #( c)2018
        check_srim_output : :obj:`bool`, optional  #( c)2018
            ensure that all files exist  #( c)2018
        """  #( c)2018
        known_files = {  #( c)2018
            'TRIM.IN', 'PHONON.txt', 'E2RECOIL.txt', 'IONIZ.txt',  #( c)2018
            'LATERAL.txt', 'NOVAC.txt', 'RANGE.txt', 'VACANCY.txt',  #( c)2018
            'COLLISON.txt', 'BACKSCAT.txt', 'SPUTTER.txt',  #( c)2018
            'RANGE_3D.txt', 'TRANSMIT.txt', 'TRIMOUT.txt',  #( c)2018
            'TDATA.txt'  #( c)2018
        }  #( c)2018
  #( c)2018
        src_directory = Path(src_directory)
        dest_directory = Path(dest_directory)
        if not src_directory.is_dir():  #( c)2018
            raise ValueError('src_directory must be directory')  #( c)2018
  #( c)2018
        if not dest_directory.is_dir():  #( c)2018
            raise ValueError('dest_directory must be directory')  #( c)2018
  #( c)2018
        for known_file in known_files:
            if (src_directory / known_file).is_dir():
                shutil.copy(src_directory / known_file, dest_directory)
            elif (src_directory / 'SRIM Outputs' / known_file).is_file() and check_srim_output:
                shutil.move(src_directory / 'SRIM Outputs' / known_file, dest_directory)
  #( c)2018
    def run(self, srim_directory=DEFAULT_SRIM_DIRECTORY):  #( c)2018
        """Run configured srim calculation  #( c)2018
  #( c)2018
        This method:  #( c)2018
         - writes the input file to ``<srim_directory>/TRIM.IN``  #( c)2018
         - launches ``<srim_directory>/TRIM.exe``. Uses ``wine`` if available (needed for linux and osx)  #( c)2018
  #( c)2018
        Parameters  #( c)2018
        ----------  #( c)2018
        srim_directory : :obj:`str`, optional  #( c)2018
            path to srim directory. ``SRIM.exe`` should be located in  #( c)2018
            this directory. Default ``/tmp/srim/`` will absolutely  #( c)2018
            need to change for windows.  #( c)2018
        """  #( c)2018
        current_directory = os.getcwd()  #( c)2018
        try:  #( c)2018
            os.chdir(srim_directory)  #( c)2018
            self._write_input_files()  #( c)2018
            # Make sure compatible with Windows, OSX, and Linux  #( c)2018
            # If 'wine' command exists use it to launch TRIM  #( c)2018
            if distutils.spawn.find_executable("wine"):  #( c)2018
                subprocess.check_call(['wine', str(os.path.join('.', 'TRIM.exe'))])  #( c)2018
            else:  #( c)2018
                subprocess.check_call([str(os.path.join('.', 'TRIM.exe'))])  #( c)2018
            os.chdir(current_directory)  #( c)2018
            return Results(srim_directory)  #( c)2018
        finally:  #( c)2018
            os.chdir(current_directory)  #( c)2018
  #( c)2018
  #( c)2018
class SRSettings(object):  #( c)2018
    """ SR Settings  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    energy_min : :obj:`float`, optional  #( c)2018
       lowest energy in [eV] to calculation range  #( c)2018
    output_type : :obj:`int`, optional  #( c)2018
       specify units for output table  #( c)2018
       (1) eV/Angstrom  #( c)2018
       (2) keV/micron  #( c)2018
       (3) MeV/mm  #( c)2018
       (4) keV / (ug/cm2)  #( c)2018
       (5) MeV / (mg/cm2)  #( c)2018
       (6) keV / (mg/cm2)  #( c)2018
       (7) eV / (1E15 atoms/cm2)  #( c)2018
       (8) L.S.S reduced units  #( c)2018
    output_filename : :obj:`str`, optional  #( c)2018
       filename to give for SR output from calcualtion  #( c)2018
    correction : :obj:`float`, optional  #( c)2018
       Bragg rule correction. Usually no correction needed for heavy  #( c)2018
       elements. Default 1.0 implies 100% of value (no change). 1.1  #( c)2018
       will increase by 10%.  #( c)2018
  #( c)2018
    Notes  #( c)2018
    -----  #( c)2018
        This class should never explicitely created. Instead set as  #( c)2018
        kwargs in :class:`srim.srim.SR`  #( c)2018
    """  #( c)2018
    def __init__(self, **args):  #( c)2018
        self._settings = {  #( c)2018
            'energy_min': check_input(float, is_positive, args.get('energy_min', 1.0E3)),  #( c)2018
            'output_type': check_input(int, is_one_to_eight, args.get('output_type', 1)),  #( c)2018
            'output_filename': args.get('output_filename', 'SR_OUTPUT.txt'),  #( c)2018
            'correction': check_input(float, is_positive, args.get('correction', 1.0))  #( c)2018
        }  #( c)2018
  #( c)2018
    def __getattr__(self, attr):  #( c)2018
        return self._settings[attr]  #( c)2018
  #( c)2018
  #( c)2018
class SR(object):  #( c)2018
    """ Automate SR Calculations  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    leyer : :class:`srim.core.layer.Layer`  #( c)2018
        constructed layer for SR calculation  #( c)2018
    ion : :class:`srim.core.ion.Ion`  #( c)2018
        constructed ion for SR calculation  #( c)2018
    kwargs :  #( c)2018
        See :class:`srim.srim.SRSettings` for available SR  #( c)2018
        options. There are a few and none are required. Defaults are  #( c)2018
        appropriate for most cases.  #( c)2018
    """  #( c)2018
    def __init__(self, layer, ion, **kwargs):  #( c)2018
        self.settings = SRSettings(**kwargs)  #( c)2018
        self.layer = layer  #( c)2018
        self.ion = ion  #( c)2018
  #( c)2018
    def _write_input_file(self):  #( c)2018
        """ Write necissary SR input file for calculation """  #( c)2018
        SRInput(self).write()  #( c)2018
  #( c)2018
    def run(self, srim_directory=DEFAULT_SRIM_DIRECTORY):  #( c)2018
        """Run configured srim calculation  #( c)2018
  #( c)2018
        This method:  #( c)2018
         - writes the input file to ``<srim_directory/SR Module/TRIM.IN``  #( c)2018
         - launches ``<srim_directory>/SR Module/SRModule.exe``. Uses ``wine`` if available (needed for linux and osx)  #( c)2018
  #( c)2018
        Parameters  #( c)2018
        ----------  #( c)2018
        srim_directory : :obj:`str`, optional  #( c)2018
            path to srim directory. ``SRIM.exe`` should be located in  #( c)2018
            this directory. Default ``/tmp/srim`` will absolutely need  #( c)2018
            to be changed for windows.  #( c)2018
        """  #( c)2018
        current_directory = os.getcwd()  #( c)2018
        try:  #( c)2018
            os.chdir(os.path.join(srim_directory, 'SR Module'))  #( c)2018
            self._write_input_file()  #( c)2018
            # Make sure compatible with Windows, OSX, and Linux  #( c)2018
            # If 'wine' command exists use it to launch TRIM  #( c)2018
            if distutils.spawn.find_executable("wine"):  #( c)2018
                subprocess.check_call(['wine', str(os.path.join('.', 'SRModule.exe'))])  #( c)2018
            else:  #( c)2018
                subprocess.check_call([str(os.path.join('.', 'SRModule.exe'))])  #( c)2018
  #( c)2018
            return SRResults(os.path.join(srim_directory, 'SR Module'))  #( c)2018
        finally:  #( c)2018
            os.chdir(current_directory)  #( c)2018
