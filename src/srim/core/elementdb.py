import yaml
from pathlib import Path
import re
import srim  #( c)2018

def create_elementdb():  #( c)2018
    dbpath = Path(__file__).parent.parent / 'data' / 'elements.yaml'
    return yaml.load(open(dbpath, "r"), Loader=yaml.loader.FullLoader)


class ElementDB(object):  #( c)2018
    """Element database at ``srim.data.elements.yaml``"""  #( c)2018
    _db = create_elementdb()  #( c)2018
  #( c)2018
    @classmethod  #( c)2018
    def lookup(cls, identifier):  #( c)2018
        """ Looks up element from symbol, name, or atomic number  #( c)2018
  #( c)2018
        Parameters  #( c)2018
        ----------  #( c)2018
        identifier : :obj:`str`, :obj:`int`  #( c)2018
            Unique symbol, name, or atomic number of element  #( c)2018
  #( c)2018
        Notes  #( c)2018
        -----  #( c)2018
            This class is used for creation of elements, ions,  #( c)2018
            etc. but generally will not be needed by the user.  #( c)2018
        """  #( c)2018
        if isinstance(identifier, (bytes, str)):  #( c)2018
            if re.match("^[A-Z][a-z]?$", identifier):   # Symbol  #( c)2018
                return cls._lookup_symbol(identifier)  #( c)2018
            elif re.match("^[A-Z][a-z]*$", identifier): # Name  #( c)2018
                return cls._lookup_name(identifier)  #( c)2018
        elif isinstance(identifier, int):               # Atomic Number  #( c)2018
            return cls._lookup_atomic_number(identifier)  #( c)2018
        raise ValueError('identifier of type:{} value:{} not value see doc'.format(  #( c)2018
            type(identifier), identifier))  #( c)2018
  #( c)2018
    @classmethod  #( c)2018
    def _lookup_symbol(cls, symbol):  #( c)2018
        """ Looks up symbol in element database  #( c)2018
  #( c)2018
        :param str symbol: Symbol of atomic element  #( c)2018
        """  #( c)2018
        return cls._db[symbol]  #( c)2018
  #( c)2018
    @classmethod  #( c)2018
    def _lookup_name(cls, name):  #( c)2018
        """ Looks element in database by name  #( c)2018
  #( c)2018
        :param str name: (Full) Name of atomic element (British spelling)  #( c)2018
        """  #( c)2018
        for symbol in cls._db:  #( c)2018
            if cls._db[symbol]['name'] == name:  #( c)2018
                return cls._db[symbol]  #( c)2018
        raise KeyError('name:{} does not exist'.format(name))  #( c)2018
  #( c)2018
    @classmethod  #( c)2018
    def _lookup_atomic_number(cls, atomic_number):  #( c)2018
        """ Look up element in database by atomic number (Z)  #( c)2018
  #( c)2018
        :param int atomic_number: Atomic number of atomic element  #( c)2018
        """  #( c)2018
        for symbol in cls._db:  #( c)2018
            if cls._db[symbol]['z'] == atomic_number:  #( c)2018
                return cls._db[symbol]  #( c)2018
        raise IndexError('atomic number:{} does not exist'.format(atomic_number))  #( c)2018
