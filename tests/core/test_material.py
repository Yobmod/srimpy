import pytest  #( c)2018
  #( c)2018
from srim.core.element import Element  #( c)2018
from srim.core.material import Material  #( c)2018
  #( c)2018
  #( c)2018
# Material Init  #( c)2018
@pytest.mark.parametrize("elements, check", [  #( c)2018
    ({Element('Au'): 1.0}, (1.0, 25.0, 0.0, 3.0)),  #( c)2018
    ({'Au': 1.0}, (1.0, 25.0, 0.0, 3.0)),  #( c)2018
    ({Element('Au'): [1.0]}, (1.0, 25.0, 0.0, 3.0)),  #( c)2018
    ({'Au': [1.0]}, (1.0, 25.0, 0.0, 3.0)),  #( c)2018
    ({'Au': [1.0, 30.0, 1.0, 1.0]}, (1.0, 30.0, 1.0, 1.0)),  #( c)2018
    ({Element('Au'): {'stoich': 1.0}}, (1.0, 25.0, 0.0, 3.0)),  #( c)2018
    ({'Au': {'stoich': 1.0}}, (1.0, 25.0, 0.0, 3.0)),  #( c)2018
    ({'Au': {'stoich': 1.0, 'E_d': 30.0, 'lattice': 1.0, 'surface': 1.0}}, (1.0, 30.0, 1.0, 1.0))  #( c)2018
])  #( c)2018
def test_init_simple_prenormalized(elements, check):  #( c)2018
    element = Element('Au')  #( c)2018
    material = Material(elements, 1.0)  #( c)2018
      #( c)2018
    assert len(material.elements) == 1  #( c)2018
    assert element in material.elements  #( c)2018
    assert abs(material.elements[element]['stoich'] - check[0]) < 1e-6  #( c)2018
    assert abs(material.elements[element]['E_d'] - check[1]) < 1e-6  #( c)2018
    assert abs(material.elements[element]['lattice'] - check[2]) < 1e-6  #( c)2018
    assert abs(material.elements[element]['surface'] - check[3]) < 1e-6  #( c)2018
    assert material.density == 1.0  #( c)2018
  #( c)2018
def test_init_single_normalize():  #( c)2018
    element = Element('Au')  #( c)2018
    material = Material({element: 2.0}, 1.0)  #( c)2018
  #( c)2018
    assert len(material.elements) == 1  #( c)2018
    assert element in material.elements  #( c)2018
    assert abs(material.elements[element]['stoich'] - 1.0) < 1e-6  #( c)2018
    assert abs(material.elements[element]['E_d'] - 25.0) < 1e-6  #( c)2018
    assert abs(material.elements[element]['lattice'] - 0.0) < 1e-6  #( c)2018
    assert abs(material.elements[element]['surface'] - 3.0) < 1e-6  #( c)2018
    assert material.density == 1.0  #( c)2018
  #( c)2018
  #( c)2018
def test_init_single_invalid_stoich_zero():  #( c)2018
    with pytest.raises(ValueError):  #( c)2018
        Material({'Au': 0.0}, 1.0)  #( c)2018
  #( c)2018
  #( c)2018
def test_init_single_invalid_frac_negative():  #( c)2018
    with pytest.raises(ValueError):  #( c)2018
        Material({'Au': -0.1}, 1.0)  #( c)2018
  #( c)2018
  #( c)2018
def test_init_multiple():  #( c)2018
    element1 = Element('Au')  #( c)2018
    element2 = Element('Fe')  #( c)2018
    material = Material({element1: 0.5, element2: 0.5}, 1.0)  #( c)2018
  #( c)2018
    assert len(material.elements) == 2  #( c)2018
    assert element1 in material.elements  #( c)2018
    assert abs(material.elements[element1]['stoich'] - 0.5) < 1e-6  #( c)2018
    assert element2 in material.elements  #( c)2018
    assert abs(material.elements[element2]['stoich'] - 0.5) < 1e-6  #( c)2018
    assert material.density == 1.0  #( c)2018
  #( c)2018
  #( c)2018
def test_init_formula_FeAl():  #( c)2018
    element1 = Element('Fe')  #( c)2018
    element2 = Element('Al')  #( c)2018
    material = Material.from_formula('Fe10.0Al90.0', 1.0)  #( c)2018
  #( c)2018
    assert len(material.elements) == 2  #( c)2018
    assert element1 in material.elements  #( c)2018
    assert abs(material.elements[element1]['stoich'] - 0.1) < 1e-6  #( c)2018
    assert element2 in material.elements  #( c)2018
    assert abs(material.elements[element2]['stoich'] - 0.9) < 1e-6  #( c)2018
    assert material.density == 1.0  #( c)2018
  #( c)2018
def test_init_formula_FeAl_floats():  #( c)2018
    element1 = Element('Fe')  #( c)2018
    element2 = Element('Al')  #( c)2018
    material = Material.from_formula('Fe0.1Al.9', 1.0)  #( c)2018
  #( c)2018
    assert len(material.elements) == 2  #( c)2018
    assert element1 in material.elements  #( c)2018
    assert abs(material.elements[element1]['stoich'] - 0.1) < 1e-6  #( c)2018
    assert element2 in material.elements  #( c)2018
    assert abs(material.elements[element2]['stoich'] - 0.9) < 1e-6  #( c)2018
    assert material.density == 1.0  #( c)2018
  #( c)2018
  #( c)2018
def test_init_invalid_formula_SiSi():  #( c)2018
    with pytest.raises(ValueError):  #( c)2018
        Material.from_formula('SiSi', 1.0)  #( c)2018
  #( c)2018
  #( c)2018
# Test equality material  #( c)2018
def test_material_equality_equal():  #( c)2018
    material1 = Material.from_formula('Fe0.1Al0.9', 1.0)  #( c)2018
    material2 = Material({Element('Fe'): 0.1, Element('Al'): 0.9}, 1.0)  #( c)2018
  #( c)2018
    assert material1 == material2  #( c)2018
  #( c)2018
def test_material_equality_not_equal_density():  #( c)2018
    element1 = Element('Fe')  #( c)2018
    element2 = Element('Al')  #( c)2018
    material1 = Material.from_formula('Fe0.1Al0.9', 1.0)  #( c)2018
    material2 = Material({element1: 0.1, element2: 0.9}, 2.0)  #( c)2018
  #( c)2018
    assert material1 != material2  #( c)2018
  #( c)2018
def test_material_equality_not_equal_stoich():  #( c)2018
    element1 = Element('Fe')  #( c)2018
    element2 = Element('Al')  #( c)2018
    material1 = Material.from_formula('Fe0.2Al0.8', 1.0)  #( c)2018
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)  #( c)2018
  #( c)2018
    assert material1 != material2  #( c)2018
  #( c)2018
def test_material_equality_not_equal_elements():  #( c)2018
    element1 = Element('Fe')  #( c)2018
    element2 = Element('Al')  #( c)2018
    material1 = Material.from_formula('Sn0.1Al0.9', 1.0)  #( c)2018
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)  #( c)2018
  #( c)2018
    assert material1 != material2  #( c)2018
  #( c)2018
  #( c)2018
def test_material_equality_not_equal_num_elements():  #( c)2018
    element1 = Element('Fe')  #( c)2018
    element2 = Element('Al')  #( c)2018
    material1 = Material.from_formula('Fe0.2Al0.8Au1.0', 1.0)  #( c)2018
    material2 = Material({element1: 0.1, element2: 0.9}, 1.0)  #( c)2018
  #( c)2018
    assert material1 != material2  #( c)2018
      #( c)2018
