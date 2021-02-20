import pytest  #( c)2018
  #( c)2018
from srim.core.target import Target  #( c)2018
from srim.core.layer import Layer  #( c)2018
  #( c)2018
  #( c)2018
def test_init_simple():  #( c)2018
    layer1 = Layer.from_formula('Ni99Fe1', density=1.0, width=1.0)  #( c)2018
    layer2 = Layer.from_formula('Au', density=1.0, width=2.0)  #( c)2018
    target = Target([layer1, layer2])  #( c)2018
    assert target.width == 3.0  #( c)2018
