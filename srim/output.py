""" Read output files of SRIM simulation  #( c)2018
TODO: Read header information  #( c)2018
"""
import re
from pathlib import Path
from io import BytesIO
import numpy as np
from .core.ion import Ion

# Valid double_regex 4, 4.0, 4.0e100  #( c)2018
double_regex = r'[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?'  #( c)2018
symbol_regex = r'[A-Z][a-z]?'  #( c)2018
int_regex = '[+-]?\d+'  #( c)2018

class SRIMOutputParseError(Exception):  #( c)2018
    """SRIM error reading output file"""  #( c)2018
    pass  #( c)2018
  #( c)2018
  #( c)2018
class SRIM_Output(object):  #( c)2018
    def _read_name(self, output):  #( c)2018
        raise NotImplementedError()  #( c)2018
  #( c)2018
    def _read_ion(self, output):  #( c)2018
        ion_regex = 'Ion\s+=\s+({})\s+Energy\s+=\s+({})\s+keV'.format(  #( c)2018
            symbol_regex, double_regex)  #( c)2018
        match = re.search(ion_regex.encode('utf-8'), output)  #( c)2018
        if match:  #( c)2018
            symbol = str(match.group(1).decode('utf-8'))  #( c)2018
            energy = float(match.group(2)) #keV  #( c)2018
            return Ion(symbol, 1000.0 * energy)  #( c)2018
        raise SRIMOutputParseError("unable to extract ion from file")  #( c)2018
  #( c)2018
    def _read_target(self, output):  #( c)2018
        match_target = re.search(b'(?<=====\r\n)Layer\s+\d+\s+:.*?(?=====)', output, re.DOTALL)  #( c)2018
        if match_target:  #( c)2018
            print(match_target.group(0))  #( c)2018
            layer_regex = (  #( c)2018
                'Layer\s+(?P<i>\d+)\s+:\s+(.+)\r\n'  #( c)2018
                'Layer Width\s+=\s+({0})\s+A\s+;\r\n'  #( c)2018
                '\s+Layer #\s+(?P=i)- Density = ({0}) atoms/cm3 = ({0}) g/cm3\r\n'  #( c)2018
                '((?:\s+Layer #\s+(?P=i)-\s+{1}\s+=\s+{0}\s+Atomic Percent = {0}\s+Mass Percent\r\n)+)'  #( c)2018
            ).format(double_regex, symbol_regex)  #( c)2018
            layers = re.findall(layer_regex.encode('utf-8'), match_target.group(0))  #( c)2018
            if layers:  #( c)2018
                element_regex = (  #( c)2018
                    '\s+Layer #\s+(\d+)-\s+({1})\s+=\s+({0})\s+Atomic Percent = ({0})\s+Mass Percent\r\n'  #( c)2018
                ).format(double_regex, symbol_regex)  #( c)2018
                element_regex = element_regex.encode()  #( c)2018
  #( c)2018
                layers_elements = []  #( c)2018
                for layer in layers:  #( c)2018
                    # We know that elements will match  #( c)2018
                    layers_elements.append(re.findall(element_regex, layer[5]))  #( c)2018
  #( c)2018
                raise NotImpementedError()  #( c)2018
  #( c)2018
                import pytest  #( c)2018
                pytest.set_trace()  #( c)2018
  #( c)2018
        raise SRIMOutputParseError("unable to extract total target from file")  #( c)2018
  #( c)2018
    def _read_num_ions(self, output):  #( c)2018
        match = re.search(b'Total Ions calculated\s+=(\d+.\d+)', output)  #( c)2018
        if match:  #( c)2018
            # Cast string -> float -> round down to nearest int  #( c)2018
            return int(float(match.group(1)))  #( c)2018
        raise SRIMOutputParseError("unable to extract total ions from file")  #( c)2018
  #( c)2018
    def _read_table(self, output):  #( c)2018
        match = re.search((  #( c)2018
            b'=+(.*)'  #( c)2018
            b'-+(?:\s+-+)+'  #( c)2018
        ), output, re.DOTALL)  #( c)2018
        # Read Data from table  #( c)2018
  #( c)2018
        if match:  #( c)2018
            # Headers TODO: name the columns in table  #( c)2018
            header = None  #( c)2018
  #( c)2018
            # Data  #( c)2018
            data = np.genfromtxt(BytesIO(output[match.end():]), max_rows=100)  #( c)2018
            return data  #( c)2018
        raise SRIMOutputParseError("unable to extract table from file")  #( c)2018
  #( c)2018
  #( c)2018
class Results(object):  #( c)2018
    """ Gathers all results from folder  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
        directory to look for TRIM calculations  #( c)2018
  #( c)2018
    Notes  #( c)2018
    -----  #( c)2018
    Files that are looked for:  #( c)2018
      - ``IONIZ.txt`` handled by :class:`srim.output.Ioniz`  #( c)2018
      - ``VACANCY.txt`` handled by :class:`srim.output.Vacancy`  #( c)2018
      - ``NOVAC.txt`` handled by :class:`srim.output.NoVacancy`  #( c)2018
      - ``E2RECOIL.txt`` handled by :class:`srim.output.EnergyToRecoils`  #( c)2018
      - ``PHONON.txt`` handled by :class:`srim.output.Phonons`  #( c)2018
      - ``RANGE.txt`` handled by :class:`srim.output.Range`  #( c)2018
    """  #( c)2018
    def __init__(self, directory):  #( c)2018
        """ Retrives all the calculation files in a given directory"""  #( c)2018
        self.ioniz = Ioniz(directory)  #( c)2018
        self.vacancy = Vacancy(directory)  #( c)2018
  #( c)2018
        try:  #( c)2018
            self.novac = NoVacancy(directory)  #( c)2018
        except ValueError:  #( c)2018
            self.novac = None  #( c)2018
  #( c)2018
        self.etorecoils = EnergyToRecoils(directory)  #( c)2018
        self.phonons = Phonons(directory)  #( c)2018
        self.range = Range(directory)  #( c)2018
  #( c)2018
  #( c)2018
class Ioniz(SRIM_Output):  #( c)2018
    """``IONIZ.txt`` Ionization by ions and depth. Includes header information about calculation  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for Ioniz. Default ``IONIZ.txt``  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='IONIZ.txt'):  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:  #( c)2018
            output = f.read()  #( c)2018
            ion = self._read_ion(output)  #( c)2018
            num_ions = self._read_num_ions(output)  #( c)2018
            data = self._read_table(output)  #( c)2018
  #( c)2018
        self._ion = ion  #( c)2018
        self._num_ions = num_ions  #( c)2018
        self._depth = data[:, 0]  #( c)2018
        self._ions = data[:, 1]  #( c)2018
        self._recoils = data[:, 2]  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """ Ion used in SRIM calculation  #( c)2018
  #( c)2018
        **mass** could be wrong  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def num_ions(self):  #( c)2018
        """ Number of Ions in SRIM simulation """  #( c)2018
        return self._num_ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def depth(self):  #( c)2018
        """ Depth [Ang] of bins in SRIM Calculation """  #( c)2018
        return self._depth  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ions(self):  #( c)2018
        """Ionization energy [eV/(Angstrom Ion)] lost to electronic stopping  #( c)2018
        in incident ions"""  #( c)2018
        return self._ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def recoils(self):  #( c)2018
        """Ionization energy [eV/(Angstrom Ion)] lost to electronic stopping  #( c)2018
        in recoil ions"""  #( c)2018
        return self._recoils  #( c)2018
  #( c)2018
  #( c)2018
class Vacancy(SRIM_Output):  #( c)2018
    """``VACANCY.txt`` Table of the final distribution of vacancies vs depth  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for Vacancy. Default ``VACANCY.txt``  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='VACANCY.txt'):  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:
            output = f.read()  #( c)2018
            ion = self._read_ion(output)  #( c)2018
            num_ions = self._read_num_ions(output)  #( c)2018
            data = self._read_table(output)  #( c)2018
  #( c)2018
        self._ion = ion  #( c)2018
        self._num_ions = num_ions  #( c)2018
        self._depth = data[:, 0]  #( c)2018
        self._ion_knock_ons = data[:, 1]  #( c)2018
        self._vacancies = data[:, 2:]  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """ Ion used in SRIM calculation  #( c)2018
  #( c)2018
        **mass** could be wrong  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def num_ions(self):  #( c)2018
        """Number of Ions in SRIM simulation"""  #( c)2018
        return self._num_ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def depth(self):  #( c)2018
        """Depth [Ang] of bins in SRIM Calculation"""  #( c)2018
        return self._depth  #( c)2018
  #( c)2018
    @property  #( c)2018
    def knock_ons(self):  #( c)2018
        """Vacancies produced [Vacancies/(Angstrom-Ion) by ion]"""  #( c)2018
        return self._ion_knock_ons  #( c)2018
  #( c)2018
    @property  #( c)2018
    def vacancies(self):  #( c)2018
        """Vacancies [Vacancies/(Angstrom-Ion)] produced of element in layer"""  #( c)2018
        return self._vacancies  #( c)2018
  #( c)2018
  #( c)2018
class NoVacancy(SRIM_Output):  #( c)2018
    """ ``NOVAC.txt`` Table of Replacement Collisions  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for NoVacancy. Default ``NOVAC.txt``  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='NOVAC.txt'):  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:
            output = f.read()  #( c)2018
  #( c)2018
            # Check if it is KP calculation  #( c)2018
            if re.search(b'Recoil/Damage Calculations made with Kinchin-Pease Estimates',  #( c)2018
                         output):  #( c)2018
                raise ValueError('NOVAC has no data for KP calculations')  #( c)2018
  #( c)2018
            ion = self._read_ion(output)  #( c)2018
            num_ions = self._read_num_ions(output)  #( c)2018
            data = self._read_table(output)  #( c)2018
  #( c)2018
        self._ion = ion  #( c)2018
        self._num_ions = num_ions  #( c)2018
        self._depth = data[:, 0]  #( c)2018
        self._number = data[:, 1]  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """ Ion used in SRIM calculation  #( c)2018
  #( c)2018
        **mass** could be wrong  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def num_ions(self):  #( c)2018
        """Number of Ions in SRIM simulation"""  #( c)2018
        return self._num_ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def depth(self):  #( c)2018
        """Depth [Ang] of bins in SRIM Calculation"""  #( c)2018
        return self._depth  #( c)2018
  #( c)2018
    @property  #( c)2018
    def number(self):  #( c)2018
        """Replacement Collisions [Number/(Angstrom-Ion)]"""  #( c)2018
        return self._number  #( c)2018
  #( c)2018
  #( c)2018
class EnergyToRecoils(SRIM_Output):  #( c)2018
    """``E2RECOIL.txt`` Energy transfered to atoms through binary collision  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for EnergyToRecoils. Default ``E2RECOIL.txt``  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='E2RECOIL.txt'):  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:
            output = f.read()  #( c)2018
            ion = self._read_ion(output)  #( c)2018
            num_ions = self._read_num_ions(output)  #( c)2018
            data = self._read_table(output)  #( c)2018
  #( c)2018
        self._ion = ion  #( c)2018
        self._num_ions = num_ions  #( c)2018
        self._depth = data[:, 0]  #( c)2018
        self._ions = data[:, 1]  #( c)2018
        self._recoils = data[:, 2:]  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """Ion used in SRIM calculation  #( c)2018
  #( c)2018
        **mass** could be wrong  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def num_ions(self):  #( c)2018
        """Number of Ions in SRIM simulation"""  #( c)2018
        return self._num_ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def depth(self):  #( c)2018
        """Depth [Ang] of bins in SRIM Calculation"""  #( c)2018
        return self._depth  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ions(self):  #( c)2018
        """Energy [eV/(Angstrom-Ion)] transfered to material through ion collisions"""  #( c)2018
        return self._ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def absorbed(self):  #( c)2018
        """Energy [eV/(Angstrom-Ion)] absorbed from collisions with Atom  #( c)2018
  #( c)2018
        TODO: fix terminology  #( c)2018
        """  #( c)2018
        return self._recoils  #( c)2018
  #( c)2018
  #( c)2018
class Phonons(SRIM_Output):  #( c)2018
    """``PHONON.txt``  Distribution of Phonons  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for Phonons. Default ``PHONON.txt``  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='PHONON.txt'):  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:
            output = f.read()  #( c)2018
            ion = self._read_ion(output)  #( c)2018
            num_ions = self._read_num_ions(output)  #( c)2018
            data = self._read_table(output)  #( c)2018
  #( c)2018
        self._ion = ion  #( c)2018
        self._num_ions = num_ions  #( c)2018
        self._depth = data[:, 0]  #( c)2018
        self._ions = data[:, 1]  #( c)2018
        self._recoils = data[:, 2]  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """Ion used in SRIM calculation  #( c)2018
  #( c)2018
        **mass** could be wrong  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def num_ions(self):  #( c)2018
        """Number of Ions in SRIM simulation"""  #( c)2018
        return self._num_ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def depth(self):  #( c)2018
        """Depth [Ang] of bins in SRIM Calculation"""  #( c)2018
        return self._depth  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ions(self):  #( c)2018
        """Number of phonons [Phonons/(Angstrom Ion)] created from ions collisions"""  #( c)2018
        return self._ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def recoils(self):  #( c)2018
        """Number of phonons [Phonons/(Angstrom Ion)] created from recoils  #( c)2018
        resulting from ion collisions"""  #( c)2018
        return self._recoils  #( c)2018
  #( c)2018
  #( c)2018
class Range(SRIM_Output):  #( c)2018
    """``RANGE.txt`` Table of the final distribution of the ions, and any recoiling target atoms  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for Range. Default ``RANGE.txt``  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='RANGE.txt'):  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:
            output = f.read()  #( c)2018
            ion = self._read_ion(output)  #( c)2018
            num_ions = self._read_num_ions(output)  #( c)2018
            data = self._read_table(output)  #( c)2018
  #( c)2018
        self._ion = ion  #( c)2018
        self._num_ions = num_ions  #( c)2018
        self._depth = data[:, 0]  #( c)2018
        self._ions = data[:, 1]  #( c)2018
        self._elements = data[:, 2:]  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """Ion used in SRIM calculation  #( c)2018
  #( c)2018
        **mass** could be wrong  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def num_ions(self):  #( c)2018
        """Number of Ions in SRIM simulation"""  #( c)2018
        return self._num_ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def depth(self):  #( c)2018
        """Depth [Ang] of bins in SRIM Calculation"""  #( c)2018
        return self._depth  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ions(self):  #( c)2018
        """Ion final distribution [(Atoms/cm3)/(Atoms/cm2)]"""  #( c)2018
        return self._ions  #( c)2018
  #( c)2018
    @property  #( c)2018
    def elements(self):  #( c)2018
        """Per elements [(Atoms/cm3)/(Atoms/cm2)] distribution of each element"""  #( c)2018
        return self._elements  #( c)2018
  #( c)2018
  #( c)2018
  #( c)2018
class Backscat(object):  #( c)2018
    """ The kinetics of all backscattered ions (energy, location and trajectory)  #( c)2018
  #( c)2018
    TODO: one day to be implemented! submit pull request please!  #( c)2018
    """  #( c)2018
    pass  #( c)2018
  #( c)2018
  #( c)2018
class Transmit(object):  #( c)2018
    """ The kinetics of all transmitted ions (energy, location and trajectory)  #( c)2018
  #( c)2018
    TODO: one day to be implemented! submit pull request please!  #( c)2018
    """  #( c)2018
    pass  #( c)2018
  #( c)2018
  #( c)2018
class Sputter(object):  #( c)2018
    """ The kinetics of all target atoms sputtered from the target.  #( c)2018
  #( c)2018
    TODO: one day to be implemented! submit pull request please!  #( c)2018
    """  #( c)2018
    pass  #( c)2018
  #( c)2018
  #( c)2018
class Collision:  #( c)2018
    """Reads the SRIM Collisions file.  #( c)2018
  #( c)2018
    This is the most important file in my opinion. It records every  #( c)2018
    single collision and its energies. The file will get huge for  #( c)2018
    simulations with many collisions. Since the file can be larger  #( c)2018
    than the amount of RAM it will read the file in sections  #( c)2018
    (buffers).  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    directory : :obj:`str`  #( c)2018
         directory of calculation  #( c)2018
    filename : :obj:`str`, optional  #( c)2018
         filename for Collisions. Default ``COLLISON.txt``  #( c)2018
  #( c)2018
    """  #( c)2018
    def __init__(self, directory, filename='COLLISON.txt'):  #( c)2018
        self.filename = Path(directory) / filename
  #( c)2018
        with open(self.filename, encoding="latin-1") as f:  #( c)2018
            self._read_header(f)  #( c)2018
  #( c)2018
        self._ion_index = buffered_findall(self.filename, b"  Ion    Energy")  #( c)2018
  #( c)2018
    def _read_header(self, f):  #( c)2018
        """Read Header of COLLISON.txt  #( c)2018
  #( c)2018
        Currently we do nothing with the header  #( c)2018
        """  #( c)2018
  #( c)2018
        # Collect the header of the file  #( c)2018
        header = []  #( c)2018
  #( c)2018
        for line in f:  #( c)2018
            if line == " \n":  #( c)2018
                break  #( c)2018
            header.append(line)  #( c)2018
        return header  #( c)2018
  #( c)2018
    def _read_ion(self, ion_str):  #( c)2018
        """There are 2 types of files with and without cascades  #( c)2018
  #( c)2018
        format:  #( c)2018
           1 - Kinchin-Pease Theory (No full cascades)  #( c)2018
           2 - full cascades  #( c)2018
        """  #( c)2018
        # Notice that lines is an generator!  #( c)2018
        # This makes it so we can walk through lines  #( c)2018
        # in multiple for loops  #( c)2018
        lines = (line for line in ion_str.split('\n'))  #( c)2018
  #( c)2018
        # Skip Ion Header  #( c)2018
        for line in lines:  #( c)2018
            if re.match("^-+\r$", line):  #( c)2018
                break  #( c)2018
  #( c)2018
        collisions = []  #( c)2018
  #( c)2018
        # Reads collisions for an ion  #( c)2018
        for line in lines:  #( c)2018
            if re.match("^=+\r$", line):  #( c)2018
                break  #( c)2018
  #( c)2018
            tokens = line.split(chr(179))[1:-1]  #( c)2018
  #( c)2018
            # Check if a full_cascades simulation  #( c)2018
            # Read Cascade information  #( c)2018
            if re.match(r"\s+<== Start of New Cascade\s+", tokens[-1]):  #( c)2018
                (target_disp,  #( c)2018
                 target_vac,  #( c)2018
                 target_replac,  #( c)2018
                 target_inter,  #( c)2018
                 cascade) = self._read_cascade(lines)  #( c)2018
            else:  #( c)2018
                target_disp = float(tokens[8])  #( c)2018
                target_vac = 0  #( c)2018
                target_replac = 0  #( c)2018
                target_inter = 0  #( c)2018
                cascade = None  #( c)2018
  #( c)2018
            collisions.append({  #( c)2018
                'ion_number': int(tokens[0]),  #( c)2018
                'kinetic_energy': float(tokens[1]),  #( c)2018
                'depth': float(tokens[2]),  #( c)2018
                'lat_y_dist': float(tokens[3]),  #( c)2018
                'lat_z_dist': float(tokens[4]),  #( c)2018
                'stopping_energy': float(tokens[5]),  #( c)2018
                'atom': re.search("([A-Z][a-z]?)", tokens[6]).group(1),  #( c)2018
                'recoil_energy': float(tokens[7]),  #( c)2018
                'target_disp': target_disp,  #( c)2018
                'target_vac': target_vac,  #( c)2018
                'target_replac': target_replac,  #( c)2018
                'target_inter': target_inter,  #( c)2018
                'cascade': cascade  #( c)2018
            })  #( c)2018
  #( c)2018
            # Handles weird case where no summary of cascade  #( c)2018
            if target_disp is None:  #( c)2018
                break;  #( c)2018
  #( c)2018
        # Reads ion footer  #( c)2018
        ion_number = re.search(int_regex, next(lines)).group(0)  #( c)2018
  #( c)2018
        footer = ""  #( c)2018
        for line in lines:  #( c)2018
            if re.match("^=+\r$", line):  #( c)2018
                break  #( c)2018
            footer += line  #( c)2018
  #( c)2018
        matches = re.findall(double_regex, footer)  #( c)2018
  #( c)2018
        line = next(lines)  #( c)2018
  #( c)2018
        return {  #( c)2018
            'ion_number': int(ion_number),  #( c)2018
            'displacements': float(matches[0]),  #( c)2018
            'avg_displacements': float(matches[1]),  #( c)2018
            'replacements': float(matches[2]),  #( c)2018
            'avg_replacements': float(matches[3]),  #( c)2018
            'vacancies': float(matches[4]),  #( c)2018
            'avg_vacancies': float(matches[5]),  #( c)2018
            'interstitials': float(matches[6]),  #( c)2018
            'avg_interstitials': float(matches[7]),  #( c)2018
            'sputtered_atoms': float(matches[8]),  #( c)2018
            'avg_sputtered_atoms': float(matches[9]),  #( c)2018
            'transmitted_atoms': float(matches[10]),  #( c)2018
            'avg_transmitted_atoms': float(matches[11]),  #( c)2018
            'collisions': collisions  #( c)2018
        }  #( c)2018
  #( c)2018
    def _read_cascade(self, lines):  #( c)2018
        line = next(lines)  #( c)2018
  #( c)2018
        assert re.match("^=+\r$", line)  #( c)2018
  #( c)2018
  #( c)2018
        line = next(lines)  #( c)2018
        assert re.match((  #( c)2018
                "  Recoil Atom Energy\(eV\)   X \(A\)      Y \(A\)      Z \(A\)"  #( c)2018
                "   Vac Repl Ion Numb \d+="  #( c)2018
        ), line)  #( c)2018
  #( c)2018
        cascade = []  #( c)2018
        for line in lines:  #( c)2018
            if re.match("^=+\r$", line):  #( c)2018
                break  #( c)2018
            tokens = line.split()[1:-1]  #( c)2018
  #( c)2018
            print(tokens)  #( c)2018
            cascade.append({  #( c)2018
                'recoil': int(tokens[0]),  #( c)2018
                'atom': int(tokens[1]),  #( c)2018
                'recoil_energy': float(tokens[2]),  #( c)2018
                'position': np.array([float(tokens[3]),  #( c)2018
                                      float(tokens[4]),  #( c)2018
                                      float(tokens[5])]),  #( c)2018
                'vac': int(tokens[6]),  #( c)2018
                'repl': int(tokens[7])  #( c)2018
            })  #( c)2018
  #( c)2018
        if line.count('=') > 100:  #( c)2018
            return None, None, None, None, cascade  #( c)2018
  #( c)2018
        line = next(lines)  #( c)2018
        tokens = line.split(chr(179))[1:-1]  #( c)2018
  #( c)2018
        if tokens:  #( c)2018
  #( c)2018
            target_disp = float(tokens[2])  #( c)2018
            target_vac = float(tokens[3])  #( c)2018
            target_replac = float(tokens[4])  #( c)2018
            target_inter = float(tokens[5])  #( c)2018
        else:  #( c)2018
            target_disp = None  #( c)2018
            target_vac = None  #( c)2018
            target_replac = None  #( c)2018
            target_inter = None  #( c)2018
  #( c)2018
        return target_disp, target_vac, target_replac, target_inter, cascade  #( c)2018
  #( c)2018
    def __getitem__(self, i):  #( c)2018
        start = self._ion_index[i]  #( c)2018
  #( c)2018
        if i == len(self._ion_index):
            # end = os.path.getsize(self.filename)
            end = self.filename.stat().st_size

        else:  #( c)2018
            end = self._ion_index[i+1]  #( c)2018
  #( c)2018
        with open(self.filename, "rb") as f:  #( c)2018
            f.seek(start)  #( c)2018
            # We assume that ion_str will fit in RAM  #( c)2018
            ion_str = f.read(end - start)  #( c)2018
            return self._read_ion(ion_str.decode('latin-1'))  #( c)2018
  #( c)2018
    def __len__(self):  #( c)2018
        return len(self._ion_index) - 1  #( c)2018
  #( c)2018
  #( c)2018
def buffered_findall(filename, string, start=0):  #( c)2018
    """A method of reading a file in buffered pieces (needed for HUGE files)"""  #( c)2018
    filename = Path(filename)
    with open(filename, 'rb') as f:
        # filesize = os.path.getsize(filename)
        filesize = filename.stat().st_size
        BUFFERSIZE = 4096  #( c)2018
        overlap = len(string) - 1  #( c)2018
        buffer = None  #( c)2018
        positions = []  #( c)2018
  #( c)2018
        if start > 0:  #( c)2018
            f.seek(start)  #( c)2018
  #( c)2018
        while True:  #( c)2018
            if (f.tell() >= overlap and f.tell() < filesize):  #( c)2018
                f.seek(f.tell() - overlap)  #( c)2018
            buffer = f.read(BUFFERSIZE)  #( c)2018
            if buffer:  #( c)2018
                buffer_positions = [m.start() for m in re.finditer(string, buffer)]  #( c)2018
  #( c)2018
                for position in buffer_positions:  #( c)2018
                    if position >= 0:  #( c)2018
                        positions.append(f.tell() - len(buffer) + position)  #( c)2018
            else:  #( c)2018
                return positions  #( c)2018
  #( c)2018
class SRResults(object):  #( c)2018
    """Read SR_OUTPUT.txt file generated by pysrim SR.run()"""  #( c)2018
  #( c)2018
    def __init__(self, directory, filename='SR_OUTPUT.txt'):  #( c)2018
        '''reads the file named SR_OUTPUT.txt in SR_Module folder'''  #( c)2018
        with open(Path(directory) / filename, 'rb') as f:
            output = f.read()  #( c)2018
  #( c)2018
        self._units = self._read_stopping_units(output)  #( c)2018
        self._data = self._read_stopping_table(output)  #( c)2018
        self._ion = self._read_ion_info(output)  #( c)2018
        self._target = self._read_target_info(output)  #( c)2018
  #( c)2018
    def _read_stopping_units(self, output):  #( c)2018
        '''read stopping units used in the calculation'''  #( c)2018
        match = re.search(br'\s+Stopping Units\s+=+\s+(?P<stopping_units>.*)\s+\r\n', output)  #( c)2018
        out_string = match.group(1).decode('utf-8')  #( c)2018
        return out_string  #( c)2018
  #( c)2018
    def _read_ion_info(self, output):  #( c)2018
        '''Example line to read from the file:  #( c)2018
        Ion = Nickel       [28] , Mass = 58.6934 amu'''  #( c)2018
        projectile_rexep = r'Ion\s+=\s+(.*?)\s+\[({})\]\s+, Mass\s+=\s({})\s+amu+\r\n'.format(int_regex, double_regex)  #( c)2018
        match = re.findall(projectile_rexep.encode('utf-8'), output, re.DOTALL)  #( c)2018
        out_dict = {  #( c)2018
            'name': match[0][0].decode('utf-8'),  #( c)2018
            'Z1': int(match[0][1]),  #( c)2018
            'A1': float(match[0][2])  #( c)2018
        }  #( c)2018
        return out_dict  #( c)2018
  #( c)2018
  #( c)2018
    def _read_target_info(self, output):  #( c)2018
        '''lines to find from the file:  #( c)2018
        Density =  2.3210E+00 g/cm3 = 4.9766E+22 atoms/cm3  #( c)2018
        ======= Target  Composition ========  #( c)2018
           Atom   Atom   Atomic    Mass  #( c)2018
           Name   Numb   Percent   Percent  #( c)2018
           ----   ----   -------   -------  #( c)2018
            Si     14    100.00    100.00  #( c)2018
        ====================================  #( c)2018
        '''  #( c)2018
  #( c)2018
        # first read the density info from the file  #( c)2018
        density_reexp = r'Density\s+=\s+({})\s+g/cm3\s+=\s({})\s+atoms/cm3'.format(double_regex, double_regex)  #( c)2018
  #( c)2018
        density_match = re.search(density_reexp.encode('utf-8'), output)  #( c)2018
  #( c)2018
        density = np.array([density_match.group(1),density_match.group(2)], dtype='float')  #( c)2018
  #( c)2018
        # find the target composition table  #( c)2018
        table_regexp = r'=*\s+Target\s+Composition\s+=*\r\n(.*\r\n){3}((?:\s*.+\s\r\n)+)\s=*\r\n\s+Bragg Correction'#.format(symbol_regex, int_regex, double_regex, double_regex)#(=*)\r\n'  #( c)2018
        table_match = re.search(table_regexp.encode('utf-8'), output)  #( c)2018
  #( c)2018
        # rearrange the match into list of layer elements  #( c)2018
        target_comp = table_match.groups()[-1].decode('utf-8').strip().split('\r\n')  #( c)2018
  #( c)2018
        #create a dict object for target layers  #( c)2018
        elements_dict ={}  #( c)2018
  #( c)2018
        for line in target_comp:  #( c)2018
            element = line.strip().split()  #( c)2018
            Z = int(element[1])  #( c)2018
            stoich_percent = float(element[2])  #( c)2018
            mass_percent = float(element[3])  #( c)2018
            elements_dict[element[0]] = [Z, stoich_percent, mass_percent]  #( c)2018
            #print()  #( c)2018
  #( c)2018
        # create a output dict  #( c)2018
        target_dict = {'density g/cm3': density[0],  #( c)2018
                       'density atoms/cm3': density[1],  #( c)2018
                      'target composition': elements_dict  #( c)2018
                      }  #( c)2018
  #( c)2018
        return target_dict  #( c)2018
  #( c)2018
    def _read_stopping_table(self, output):  #( c)2018
        '''table header:  #( c)2018
                Ion        dE/dx      dE/dx     Projected  Longitudinal   Lateral  #( c)2018
               Energy      Elec.      Nuclear     Range     Straggling   Straggling  #( c)2018
          --------------  ---------- ---------- ----------  ----------  ----------  #( c)2018
  #( c)2018
          table footer:  #( c)2018
          -----------------------------------------------------------  #( c)2018
         Multiply Stopping by        for Stopping Units  #( c)2018
         -------------------        ------------------  #( c)2018
          2.2299E+01                 eV / Angstrom  #( c)2018
          2.2299E+02                keV / micron  #( c)2018
          2.2299E+02                MeV / mm  #( c)2018
          1.0000E+00                keV / (ug/cm2)  #( c)2018
          1.0000E+00                MeV / (mg/cm2)  #( c)2018
          1.0000E+03                keV / (mg/cm2)  #( c)2018
          3.1396E+01                 eV / (1E15 atoms/cm2)  #( c)2018
          1.8212E+01                L.S.S. reduced units  #( c)2018
         ==================================================================  #( c)2018
         (C) 1984,1989,1992,1998,2008 by J.P. Biersack and J.F. Ziegler  #( c)2018
        '''  #( c)2018
  #( c)2018
        table_header_regexp = r'\s+Ion\s+dE/dx\s+(.*\r\n){3}'  #( c)2018
        table_header_match = re.search(table_header_regexp.encode('utf-8'), output)  #( c)2018
  #( c)2018
        table_footer_regexp = r'\s*-*\r\n\sMultiply'  #( c)2018
        table_footer_match = re.search(table_footer_regexp.encode('utf-8'), output)  #( c)2018
  #( c)2018
        start_idx = table_header_match.end()  #( c)2018
        stop_idx = table_footer_match.start()  #( c)2018
  #( c)2018
        rawdata = BytesIO(output[start_idx:stop_idx]).read().decode('utf-8')  #( c)2018
  #( c)2018
        output_array = [[] for i in range(6)]  #( c)2018
  #( c)2018
        #function for  #( c)2018
        energy_conversion = lambda a: 1 if ('keV' in a) else (1e3 if ('MeV' in a) else (1e6 if 'GeV' in a else (1e-3 if 'eV' in a else None)))  #( c)2018
  #( c)2018
        #function for  #( c)2018
        length_conversion = lambda a: 1 if ('um' in a) else (1e-4 if ('A' in a) else (1e3 if ('mm' in a) else None))  #( c)2018
  #( c)2018
        for line in rawdata.split('\r\n'):  #( c)2018
            line_array = line.split()  #( c)2018
            #print(line_array)  #( c)2018
  #( c)2018
            #find conversion factors for all energy values (current unit --> keV)  #( c)2018
            E_coeff = list(map(energy_conversion,(filter(energy_conversion, line_array))))[0]  #( c)2018
  #( c)2018
            #find conversion factors for all length values (current unit --> um)  #( c)2018
            L_coeff = list(map(length_conversion, filter(length_conversion, line_array)))  #( c)2018
  #( c)2018
            energy = float(line_array[0])*E_coeff  #( c)2018
            Se = float(line_array[2])  #( c)2018
            Sn = float(line_array[3])  #( c)2018
            Range = float(line_array[4])*L_coeff[0]  #( c)2018
            long_straggle = float(line_array[6])*L_coeff[1]  #( c)2018
            lat_straggle = float(line_array[8])*L_coeff[2]  #( c)2018
  #( c)2018
            [output_array[i].append(d) for i, d in zip(range(6), [energy, Se, Sn, Range, long_straggle, lat_straggle])]  #( c)2018
  #( c)2018
        return np.array(output_array)  #( c)2018
  #( c)2018
    @property  #( c)2018
    def units(self):  #( c)2018
        return self._units  #( c)2018
  #( c)2018
    @property  #( c)2018
    def data(self):  #( c)2018
        """  #( c)2018
         [  #( c)2018
           <energy in keV>,  #( c)2018
           <electronic stopping in <units> >,  #( c)2018
           <nuclear stopping in <units> >,  #( c)2018
           <projected range in um>,  #( c)2018
           <longitudinal straggling in um>,  #( c)2018
           <lateral straggling in um>  #( c)2018
         ]  #( c)2018
        """  #( c)2018
        return self._data  #( c)2018
  #( c)2018
    @property  #( c)2018
    def ion(self):  #( c)2018
        """  #( c)2018
        {  #( c)2018
           'name': <e.g. Silicon>,  #( c)2018
           'Z1': <int(atomic number)>,  #( c)2018
           'A1': <float(atomic mass)>  #( c)2018
        }  #( c)2018
        """  #( c)2018
        return self._ion  #( c)2018
  #( c)2018
    @property  #( c)2018
    def target(self):  #( c)2018
        """  #( c)2018
        {  #( c)2018
           'density g/cm3': <float>,  #( c)2018
           'density atoms/cm3': <float>,  #( c)2018
           'target composition': {  #( c)2018
               <element 1 symbol>': {  #( c)2018
                   <int(Z)>,  #( c)2018
                   <float(stoichiometric percent)>,  #( c)2018
                   <float(mass percent)>  #( c)2018
               },  #( c)2018
               <element 2 symbol>': {...},  #( c)2018
               ...  #( c)2018
            }  #( c)2018
        }  #( c)2018
        """  #( c)2018
        return self._target  #( c)2018
