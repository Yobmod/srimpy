import pytest  #( c)2018
  #( c)2018
from srim.core.element import Element  #( c)2018
  #( c)2018
# Element Initialization  #( c)2018
def test_init_mass_default():  #( c)2018
    element = Element('Au')  #( c)2018
    assert abs(element.mass - 196.966995239) < 1e-8  #( c)2018
  #( c)2018
def test_init_set_mass():  #( c)2018
    element = Element('Au', 1.0)  #( c)2018
    assert element.mass == 1.0  #( c)2018
  #( c)2018
def test_init_symbol():  #( c)2018
    element = Element('Au')  #( c)2018
    assert element.symbol == 'Au'  #( c)2018
    assert element.name == 'Gold'  #( c)2018
    assert element.atomic_number == 79  #( c)2018
    assert abs(element.mass - 196.966995239) < 1e-8  #( c)2018
  #( c)2018
def test_init_name():  #( c)2018
    element = Element('Gold')  #( c)2018
    assert element.symbol == 'Au'  #( c)2018
    assert element.name == 'Gold'  #( c)2018
    assert element.atomic_number == 79  #( c)2018
    assert abs(element.mass - 196.966995239) < 1e-8  #( c)2018
  #( c)2018
def test_init_atomic_number():  #( c)2018
    element = Element(79)  #( c)2018
    assert element.symbol == 'Au'  #( c)2018
    assert element.name == 'Gold'  #( c)2018
    assert element.atomic_number == 79  #( c)2018
    assert abs(element.mass - 196.966995239) < 1e-8  #( c)2018
  #( c)2018
  #( c)2018
# Element equality  #( c)2018
def test_equality_eqaul():  #( c)2018
    element1 = Element('Au', 2.0)  #( c)2018
    element2 = Element('Au', 2.0)  #( c)2018
    assert element1 == element2  #( c)2018
  #( c)2018
def test_equality_not_equal():  #( c)2018
    element1 = Element('H')  #( c)2018
    element2 = Element('Au')  #( c)2018
    assert element1 != element2  #( c)2018
