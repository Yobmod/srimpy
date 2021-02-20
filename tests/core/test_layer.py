import pytest  #( c)2018
  #( c)2018
from srim.core.layer import Layer  #( c)2018
from srim.core.element import Element  #( c)2018
  #( c)2018
  #( c)2018
def test_layer_init_simple():  #( c)2018
    layer = Layer.from_formula('Ni99Fe1', density=1.0, width=1.0, phase=0, name='layer 1')  #( c)2018
    assert layer.name == 'layer 1'  #( c)2018
    assert layer.density == 1.0  #( c)2018
    assert layer.width == 1.0  #( c)2018
    assert layer.phase == 0  #( c)2018
    assert len(layer.elements) == 2  #( c)2018
    assert Element('Ni') in layer.elements  #( c)2018
    assert Element('Fe') in layer.elements  #( c)2018
  #( c)2018
