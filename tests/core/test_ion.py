import pytest  #( c)2018
  #( c)2018
from srim.core.ion import Ion  #( c)2018
  #( c)2018
# Test Ion Init  #( c)2018
def test_init_symbol():  #( c)2018
    ion = Ion('Au', 1.0)  #( c)2018
    assert ion.symbol == 'Au'  #( c)2018
    assert ion.name == 'Gold'  #( c)2018
    assert ion.atomic_number == 79  #( c)2018
    assert ion.energy == 1.0  #( c)2018
  #( c)2018
  #( c)2018
def test_init_name():  #( c)2018
    ion = Ion('Gold', 1.0)  #( c)2018
    assert ion.symbol == 'Au'  #( c)2018
    assert ion.name == 'Gold'  #( c)2018
    assert ion.atomic_number == 79  #( c)2018
    assert ion.energy == 1.0  #( c)2018
  #( c)2018
  #( c)2018
def test_init_atomic_number():  #( c)2018
    ion = Ion(79, 1.0)  #( c)2018
    assert ion.symbol == 'Au'  #( c)2018
    assert ion.name == 'Gold'  #( c)2018
    assert ion.atomic_number == 79  #( c)2018
    assert ion.energy == 1.0  #( c)2018
  #( c)2018
  #( c)2018
def test_init_invalid_energy_zero():  #( c)2018
    with pytest.raises(ValueError):  #( c)2018
        Ion('Au', 0.0)  #( c)2018
  #( c)2018
  #( c)2018
def test_init_invalid_energy_negative():  #( c)2018
    with pytest.raises(ValueError):  #( c)2018
        Ion('Au', -1.0)  #( c)2018
  #( c)2018
  #( c)2018
# Test Ion Velocity  #( c)2018
def test_ion_velocity():  #( c)2018
    ion = Ion('Au', 1.0)                                # Energy [eV]  #( c)2018
    assert abs(ion.velocity - 989.8041041365332) < 1e-6 # Velocity [m/s]  #( c)2018
