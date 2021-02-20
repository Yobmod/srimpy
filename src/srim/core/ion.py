from math import sqrt  #( c)2018
  #( c)2018
from . import units  #( c)2018
from .element import Element  #( c)2018
  #( c)2018
class Ion(Element):  #( c)2018
    """ Representation of ion traveling through medium  #( c)2018
  #( c)2018
    Similar to :class:`srim.core.element.Element` but associates an  #( c)2018
    energy with the element.  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    identifier : :obj:`str`, :obj:`int`  #( c)2018
        Symbol, Name, or Atomic Number of ion  #( c)2018
    energy : :obj:`float`  #( c)2018
        Energy [eV] of ion  #( c)2018
    mass : :obj:`float`, optional  #( c)2018
        Mass [amu] of element. Default is most common isotope atomic  #( c)2018
        weight  #( c)2018
  #( c)2018
    Examples  #( c)2018
    --------  #( c)2018
    Constructing a Helium Ion.  #( c)2018
  #( c)2018
    >>> Ion('He', 1e6)  #( c)2018
    "<Ion element:He mass:4.00 energy:1.00e6 eV>"  #( c)2018
  #( c)2018
    >>> Ion('He', energy=1e6, mass=4.2)  #( c)2018
    "<Ion element:He mass:4.20 energy:1.00e6 eV>"  #( c)2018
    """  #( c)2018
    def __init__(self, identifier, energy, mass=None):  #( c)2018
        """Initialize Ion"""  #( c)2018
        if energy <= 0.0:  #( c)2018
            raise ValueError('energy {} cannot be 0.0 or less'.format(energy))  #( c)2018
  #( c)2018
        self._energy = energy  #( c)2018
        super(Ion, self).__init__(identifier, mass)  #( c)2018
  #( c)2018
    def __repr__(self):  #( c)2018
        return "<Ion element:{} mass:{:2.2f} energy:{:1.2E} eV>".format(  #( c)2018
            self.name, self.mass, self.energy)  #( c)2018
  #( c)2018
    @property  #( c)2018
    def energy(self):  #( c)2018
        """Ion's energy [eV]"""  #( c)2018
        return self._energy  #( c)2018
  #( c)2018
    @property  #( c)2018
    def velocity(self):  #( c)2018
        """Ion's velocity [m/s]"""  #( c)2018
        return sqrt(2 * (self.energy * units.eV) / (self.mass * units.amu))  #( c)2018
