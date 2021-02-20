import re  #( c)2018
  #( c)2018
from .utils import (  #( c)2018
    check_input,  #( c)2018
    is_positive, is_greater_than_zero,  #( c)2018
    is_zero_or_one  #( c)2018
)  #( c)2018
from .element import Element  #( c)2018
  #( c)2018
class Material(object):  #( c)2018
    """ Material Representation """  #( c)2018
    def __init__(self, elements, density, phase=0):  #( c)2018
        """Create Material from elements, density, and phase  #( c)2018
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
        phase : :obj:`int`  #( c)2018
             phase of material (solid = 0, gas = 1). Default solid (0).  #( c)2018
  #( c)2018
  #( c)2018
        Notes  #( c)2018
        -----  #( c)2018
        This class is more featureful that `srim.core.layer.Layer`  #( c)2018
        would lead you to believe. In general this class will not be  #( c)2018
        called by the user.  #( c)2018
  #( c)2018
        Structure of dictionary elements properties:  #( c)2018
         - stoich  (required): Stoichiometry of element (fraction)  #( c)2018
         - E_d     (optional): Displacement energy [eV] default 25.0 eV  #( c)2018
         - lattice (optional): Lattice binding energies [eV] default 0.0 eV  #( c)2018
         - surface (optional): Surface binding energies [eV] default 3.0 eV  #( c)2018
  #( c)2018
        dictionary element properties can be:  #( c)2018
  #( c)2018
        float or int: stoich  #( c)2018
          all others take default values for now  #( c)2018
  #( c)2018
        dictionary:  #( c)2018
          {'stoich', 'E_d', 'lattice', 'surface'}  #( c)2018
          stoich is required all others are optional  #( c)2018
  #( c)2018
        elements list structure:  #( c)2018
          [stoich, E_d, lattice, surface]  #( c)2018
          first element is required all others optional  #( c)2018
  #( c)2018
        For example a single element in elements can be specified as:  #( c)2018
          - {'Cu': 1.0}  #( c)2018
          - {Element('Cu'): 1.0}  #( c)2018
          - {Element('Cu'): [1.0, 25.0]}  #( c)2018
          - {'Cu': {'stoich': 1.0}}  #( c)2018
          - {Element('Cu'): {'stoich': 1.0, 'E_d': 25.0, 'lattice': 0.0, 'surface': 3.0}  #( c)2018
  #( c)2018
        All stoichiometries will be normalized to 1.0  #( c)2018
  #( c)2018
        Eventually the materials will have better defaults that come  #( c)2018
        from databases.  #( c)2018
        """  #( c)2018
        self.phase = phase  #( c)2018
        self.density = density  #( c)2018
        self.elements = {}  #( c)2018
  #( c)2018
        stoich_sum = 0.0  #( c)2018
        for element in elements:  #( c)2018
            values = elements[element]  #( c)2018
  #( c)2018
            if isinstance(values, dict):  #( c)2018
                stoich = values['stoich']  #( c)2018
                e_disp = values.get('E_d', 25.0)  #( c)2018
                lattice = values.get('lattice', 0.0)  #( c)2018
                surface = values.get('surface', 3.0)  #( c)2018
            elif isinstance(values, list):  #( c)2018
                default_values = [0.0, 25.0, 0.0, 3.0]  #( c)2018
                if len(values) == 0 or len(values) > 4:  #( c)2018
                    raise ValueError('list must be 0 < length < 5')  #( c)2018
                values = values + default_values[len(values):]  #( c)2018
                stoich, e_disp, lattice, surface = values  #( c)2018
            elif isinstance(values, (int, float)):  #( c)2018
                stoich = values  #( c)2018
                e_disp = 25.0  #( c)2018
                lattice = 0.0  #( c)2018
                surface = 3.0  #( c)2018
            else:  #( c)2018
                raise ValueError('elements must be of type int, float, list, or dict')  #( c)2018
  #( c)2018
            # Check input  #( c)2018
            stoich = check_input(float, is_greater_than_zero, stoich)  #( c)2018
            e_disp = check_input(float, is_positive, e_disp)  #( c)2018
            lattice = check_input(float, is_positive, lattice)  #( c)2018
            surface = check_input(float, is_positive, surface)  #( c)2018
  #( c)2018
            stoich_sum += stoich  #( c)2018
  #( c)2018
            if not isinstance(element, Element):  #( c)2018
                element = Element(element)  #( c)2018
  #( c)2018
            self.elements.update({element: {  #( c)2018
                'stoich': stoich, 'E_d': e_disp,  #( c)2018
                'lattice': lattice, 'surface': surface  #( c)2018
            }})  #( c)2018
  #( c)2018
        # Normalize the Chemical Composisiton to 1.0  #( c)2018
        for element in self.elements:  #( c)2018
            self.elements[element]['stoich'] /= stoich_sum  #( c)2018
  #( c)2018
  #( c)2018
    @classmethod  #( c)2018
    def from_formula(cls, chemical_formula, density, phase=0):  #( c)2018
        """ Creation Material from chemical formula string and density  #( c)2018
  #( c)2018
        Parameters  #( c)2018
        ----------  #( c)2018
        chemical_formula : :obj:`str`  #( c)2018
            chemical formula string in specific format  #( c)2018
        density : :obj:`float`  #( c)2018
            density [g/cm^3] of material  #( c)2018
        phase : :obj:`int`, optional  #( c)2018
            phase of material (solid = 0, gas = 1). Default solid (0).  #( c)2018
  #( c)2018
        Notes  #( c)2018
        -----  #( c)2018
        Examples of chemical_formula that can be used:  #( c)2018
         - SiC  #( c)2018
         - CO2  #( c)2018
         - AuFe1.5  #( c)2018
         - Al10.0Fe90.0  #( c)2018
  #( c)2018
        Chemical Formula will be normalized to 1.0  #( c)2018
        """  #( c)2018
        elements = cls._formula_to_elements(chemical_formula)  #( c)2018
        return Material(elements, density, phase)  #( c)2018
  #( c)2018
    @staticmethod  #( c)2018
    def _formula_to_elements(chemical_formula):  #( c)2018
        """ Convert chemical formula to elements """  #( c)2018
        single_element = '([A-Z][a-z]?)([0-9]*(?:\.[0-9]*)?)?'  #( c)2018
        elements = {}  #( c)2018
  #( c)2018
        if re.match('^(?:{})+$'.format(single_element), chemical_formula):  #( c)2018
            matches = re.findall(single_element, chemical_formula)  #( c)2018
        else:  #( c)2018
            error_str = 'chemical formula string {} does not match regex'  #( c)2018
            raise ValueError(error_str.format(chemical_formula))  #( c)2018
  #( c)2018
        # Check for errors in stoichiometry  #( c)2018
        for symbol, fraction in matches:  #( c)2018
            element = Element(symbol)  #( c)2018
  #( c)2018
            if element in elements:  #( c)2018
                error_str = 'cannot have duplicate elements {} in stoichiometry'  #( c)2018
                raise ValueError(error_str.format(element.symbol))  #( c)2018
  #( c)2018
            if fraction == '':  #( c)2018
                fraction = 1.0  #( c)2018
  #( c)2018
            elements.update({element: float(fraction)})  #( c)2018
        return elements  #( c)2018
  #( c)2018
    @property  #( c)2018
    def density(self):  #( c)2018
        """Material's density"""  #( c)2018
        return self._density  #( c)2018
  #( c)2018
    @density.setter  #( c)2018
    def density(self, value):  #( c)2018
        self._density = check_input(float, is_positive, value)  #( c)2018
  #( c)2018
    @property  #( c)2018
    def phase(self):  #( c)2018
        """Material's phase"""  #( c)2018
        return self._phase  #( c)2018
  #( c)2018
    @phase.setter  #( c)2018
    def phase(self, value):  #( c)2018
        self._phase = check_input(int, is_zero_or_one, value)  #( c)2018
  #( c)2018
    @property  #( c)2018
    def chemical_formula(self):  #( c)2018
        """Material's chemical formula"""  #( c)2018
        return ' '.join('{} {:1.2f}'.format(element.symbol, self.elements[element]['stoich']) for element in self.elements)  #( c)2018
  #( c)2018
    def __repr__(self):  #( c)2018
        material_str = "<Material formula:{} density:{:2.3f}>"  #( c)2018
        return material_str.format(self.chemical_formula, self.density)  #( c)2018
  #( c)2018
    def __eq__(self, material):  #( c)2018
        if abs(self.density - material.density) > 1e-6:  #( c)2018
            return False  #( c)2018
  #( c)2018
        if len(self.elements) != len(material.elements):  #( c)2018
            return False  #( c)2018
  #( c)2018
        for element in self.elements:  #( c)2018
            if not element in material.elements:  #( c)2018
                return False  #( c)2018
            for prop in self.elements[element]:  #( c)2018
                if abs(self.elements[element][prop] - material.elements[element][prop]) > 1e-6:  #( c)2018
                    return False  #( c)2018
        return True  #( c)2018
