from srim.srim import TRIM, SR  #( c)2018
from srim.core.target import Target  #( c)2018
from srim.core.layer import Layer  #( c)2018
from srim.core.ion import Ion  #( c)2018
  #( c)2018
TESTDATA_DIRECTORY = 'test_files'  #( c)2018
  #( c)2018
def test_simple_trim_init():  #( c)2018
    ion = Ion('Ni', 1.0e6)  #( c)2018
  #( c)2018
    layer = Layer.from_formula('Ni', 8.9, 1000.0)  #( c)2018
    target = Target([layer])  #( c)2018
  #( c)2018
    trim = TRIM(target, ion)  #( c)2018
  #( c)2018
  #( c)2018
def test_simple_srim_init():  #( c)2018
    # Construct a Nickel ion  #( c)2018
    ion = Ion('Xe', energy=1.2e9)  #( c)2018
  #( c)2018
    # Construct a layer of nick 20um thick with a displacement energy of 30 eV  #( c)2018
    layer = Layer({  #( c)2018
        'Si': {  #( c)2018
            'stoich': 0.5,  #( c)2018
            'E_d': 35.0, # Displacement Energy  #( c)2018
            'lattice': 0.0,  #( c)2018
            'surface': 3.0  #( c)2018
        },  #( c)2018
        'C': {  #( c)2018
            'stoich': 0.5,  #( c)2018
            'E_d': 20.0, # Displacement Energy  #( c)2018
            'lattice': 0.0,  #( c)2018
            'surface': 3.0  #( c)2018
        }  #( c)2018
    }, density=3.21, width=10000.0)  #( c)2018
  #( c)2018
    target = Target([layer])  #( c)2018
  #( c)2018
    srim = SR(layer, ion, output_type=5)  #( c)2018
  #( c)2018
    # resulting file should be equal to  #( c)2018
    # test_files/SRIM/SR_OUTPUT.txt  #( c)2018
