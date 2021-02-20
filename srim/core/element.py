from .elementdb import ElementDB  #( c)2018
  #( c)2018
class Element(object):  #( c)2018
    """ Element from periodic table  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    identifier : :obj:`str`, :obj:`int`  #( c)2018
        Symbol, Name, or Atomic Number of element  #( c)2018
    mass : :obj:`float`, optional  #( c)2018
        Mass [amu] of element. Default is most common isotope atomic  #( c)2018
        weight  #( c)2018
  #( c)2018
    Examples  #( c)2018
    --------  #( c)2018
    Constructing a Helium Atom.  #( c)2018
  #( c)2018
    >>> Element('He')  #( c)2018
    <Element symbol:He name:Helium mass:4.00>  #( c)2018
  #( c)2018
    >>> Element('Helium')  #( c)2018
    <Element symbol:He name:Helium mass:4.00>  #( c)2018
  #( c)2018
    >>> Element(2)  #( c)2018
    <Element symbol:He name:Helium mass:4.00>  #( c)2018
  #( c)2018
    >>> Element('He', 4.3)  #( c)2018
    <Element symbol:He name:Helium mass:4.30>  #( c)2018
    """  #( c)2018
    def __init__(self, identifier, mass=None):  #( c)2018
        """Initializes element from identifier and mass"""  #( c)2018
        element = ElementDB.lookup(identifier)  #( c)2018
  #( c)2018
        self._symbol = element['symbol']  #( c)2018
        self._name = element['name']  #( c)2018
        self._atomic_number = element['z']  #( c)2018
  #( c)2018
        if mass:  #( c)2018
            self._mass = mass  #( c)2018
        else:  #( c)2018
            self._mass = element['mass']  #( c)2018
  #( c)2018
    def __eq__(self, element):  #( c)2018
        if (self.symbol == element.symbol and  #( c)2018
            self.name == element.name and  #( c)2018
            self.atomic_number == element.atomic_number and  #( c)2018
            self.mass == element.mass):  #( c)2018
            return True  #( c)2018
        return False  #( c)2018
  #( c)2018
    def __repr__(self):  #( c)2018
        return "<Element symbol:{} name:{} mass:{:2.2f}>".format(  #( c)2018
            self.symbol, self.name, self.mass)  #( c)2018
  #( c)2018
    def __hash__(self):  #( c)2018
        return sum(hash(item) for item in [  #( c)2018
            self._mass, self._symbol, self._name, self.atomic_number  #( c)2018
        ])  #( c)2018
  #( c)2018
    @property  #( c)2018
    def symbol(self):  #( c)2018
        """Element's atomic symbol"""  #( c)2018
        return self._symbol  #( c)2018
  #( c)2018
    @property  #( c)2018
    def name(self):  #( c)2018
        """Element's formal name"""  #( c)2018
        return self._name  #( c)2018
  #( c)2018
    @property  #( c)2018
    def atomic_number(self):  #( c)2018
        """Element's atomic number"""  #( c)2018
        return self._atomic_number  #( c)2018
  #( c)2018
    @property  #( c)2018
    def mass(self):  #( c)2018
        """Element's mass"""  #( c)2018
        return self._mass  #( c)2018
