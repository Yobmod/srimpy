from .material import Material  #( c)2018
from .utils import check_input, is_positive  #( c)2018
  #( c)2018
class Layer(Material):  #( c)2018
    """ Represents a layer in target  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    elements : :obj:`dict`  #( c)2018
        dictionary of elements (:class:`srim.core.elements.Element`, :obj:`str`, or :obj:`int`) with properties  #( c)2018
         - ``stoich``  (float, int, required): Stoichiometry of element (fraction)  #( c)2018
         - ``E_d``     (float, int, optional): Displacement energy [eV] default 25.0 eV  #( c)2018
         - ``lattice`` (float, int, optional): Lattice binding energies [eV] default 0.0 eV  #( c)2018
         - ``surface`` (float, int, optional): Surface binding energies [eV] default 3.0 eV  #( c)2018
    density : :obj:`float`  #( c)2018
       density [g/cm^3] of material  #( c)2018
    width : :obj:`float`  #( c)2018
       width [Angstroms] of layer  #( c)2018
    phase : :obj:`int`  #( c)2018
       phase of material (solid = 0, gas = 1). Default solid (0).  #( c)2018
    name : :obj:`str:, optional  #( c)2018
       name of the Layer (defaults to chemical_formula)  #( c)2018
  #( c)2018
    Examples  #( c)2018
    --------  #( c)2018
    Construct a layer of SiC with experimental values.  #( c)2018
  #( c)2018
    >>> Layer({  #( c)2018
        'Si': {  #( c)2018
           'stoich': 0.5,  #( c)2018
           'E_d': 35.0, # Displacement Energy [eV]  #( c)2018
           'lattice': 0.0,  #( c)2018
           'surface': 3.0  #( c)2018
        },  #( c)2018
        'C': {  #( c)2018
           'stoich': 0.5,  #( c)2018
           'E_d': 20.0, # Displacement Energy [eV]  #( c)2018
           'lattice': 0.0,  #( c)2018
           'surface': 3.0  #( c)2018
    }, density=3.21, width=10000.0)  #( c)2018
    """  #( c)2018
    def __init__(self, elements, density, width, phase=0, name=None):  #( c)2018
        """Creation of Layer from elements, density, width, phase, and  #( c)2018
name"""  #( c)2018
        self.width = width  #( c)2018
        self.name = name  #( c)2018
        super(Layer, self).__init__(elements, density, phase)  #( c)2018
  #( c)2018
    @classmethod  #( c)2018
    def from_formula(cls, chemical_formula, density, width, phase=0, name=None):  #( c)2018
        """ Creation Layer from chemical formula string, density, width, phase, and name  #( c)2018
  #( c)2018
        Parameters  #( c)2018
        ----------  #( c)2018
        chemical_formula : str  #( c)2018
            see :meth:`srim.core.material.Material.from_formula` for  #( c)2018
            allowed formulas. Quite flexible.  #( c)2018
        density : :obj:`float`  #( c)2018
            density [g/cm^3] of material  #( c)2018
        width : :obj:`float`  #( c)2018
            width [Angstroms] of layer  #( c)2018
        phase : :obj:`int`  #( c)2018
            phase of material (solid = 0, gas = 1). Default solid (0).  #( c)2018
        name : :obj:`str:, optional  #( c)2018
            name of the Layer (defaults to chemical_formula)  #( c)2018
  #( c)2018
        Notes  #( c)2018
        -----  #( c)2018
            This method is not used as much since you do not have an  #( c)2018
            easy way to set the displacement energy.  #( c)2018
        """  #( c)2018
        elements = cls._formula_to_elements(chemical_formula)  #( c)2018
        return Layer(elements, density, width, phase, name)  #( c)2018
  #( c)2018
    @property  #( c)2018
    def width(self):  #( c)2018
        """Layer's width"""  #( c)2018
        return self._width  #( c)2018
  #( c)2018
    @width.setter  #( c)2018
    def width(self, value):  #( c)2018
        self._width = check_input(float, is_positive, value)  #( c)2018
  #( c)2018
    @property  #( c)2018
    def name(self):  #( c)2018
        """Layer's Name"""  #( c)2018
        if self._name:  #( c)2018
            return self._name  #( c)2018
        return self.chemical_formula  #( c)2018
  #( c)2018
    @name.setter  #( c)2018
    def name(self, value):  #( c)2018
        self._name = str(value)  #( c)2018
  #( c)2018
    def __repr__(self):  #( c)2018
        return "<Layer material:{} width:{}>".format(self.chemical_formula, self.width)  #( c)2018
