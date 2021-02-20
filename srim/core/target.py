class Target(object):  #( c)2018
    """ Target that Ion Impacts  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    layers : list  #( c)2018
        list of :class:`srim.core.layer.Layer` to construct Target  #( c)2018
  #( c)2018
    Examples  #( c)2018
    --------  #( c)2018
    Lets construct a SiC target. While only one layer is shown an  #( c)2018
    arbitrary number of them can be used.  #( c)2018
  #( c)2018
    >>> Target([Layer({  #( c)2018
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
    }, density=3.21, width=10000.0)])  #( c)2018
    """  #( c)2018
    def __init__(self, layers):  #( c)2018
        self.layers = layers  #( c)2018
  #( c)2018
    @property  #( c)2018
    def width(self):  #( c)2018
        """total width of target (sum of layers)"""  #( c)2018
        return sum(layer.width for layer in self.layers)  #( c)2018
