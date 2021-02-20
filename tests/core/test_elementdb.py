import pytest  #( c)2018
  #( c)2018
from srim.core.elementdb import ElementDB  #( c)2018
  #( c)2018
# ElementDB size  #( c)2018
def test_db_size():  #( c)2018
    assert len(ElementDB._db) == 112  #( c)2018
  #( c)2018
  #( c)2018
# ElementDB Lookups  #( c)2018
def test_lookup_symbol():  #( c)2018
    element = ElementDB._lookup_symbol('Fe')  #( c)2018
    assert element['symbol'] == 'Fe'  #( c)2018
    assert element['name'] == 'Iron'  #( c)2018
  #( c)2018
  #( c)2018
def test_lookup_invalid_symbol():  #( c)2018
    with pytest.raises(KeyError):  #( c)2018
        ElementDB._lookup_symbol('Zx')  #( c)2018
  #( c)2018
  #( c)2018
def test_lookup_name():  #( c)2018
    element = ElementDB._lookup_name('Aluminium')  #( c)2018
    assert element['symbol'] == 'Al'  #( c)2018
    assert element['name'] == 'Aluminium'  #( c)2018


def test_lookup_invalid_name():  #( c)2018
    with pytest.raises(KeyError):  #( c)2018
        ElementDB._lookup_name('Suzium') # My dog's name


def test_lookup_atomic_number():  #( c)2018
    element = ElementDB._lookup_atomic_number(100)  #( c)2018
    assert element['symbol'] == 'Fm'  #( c)2018
    assert element['name'] == 'Fermium'  #( c)2018
  #( c)2018
  #( c)2018
def test_lookup_invalid_atomic_number_negative():  #( c)2018
    with pytest.raises(IndexError):  #( c)2018
        ElementDB._lookup_atomic_number(-1)  #( c)2018
  #( c)2018
  #( c)2018
def test_lookup_invalid_atomic_number_large():  #( c)2018
    with pytest.raises(IndexError):  #( c)2018
        ElementDB._lookup_atomic_number(130)  #( c)2018
  #( c)2018
  #( c)2018
# Test lookup correct function  #( c)2018
def test_lookup_call_symbol(mocker):  #( c)2018
    mocker.patch('srim.core.elementdb.ElementDB._lookup_symbol')  #( c)2018
    ElementDB.lookup('Au')  #( c)2018
    ElementDB._lookup_symbol.assert_called_once_with('Au')  #( c)2018
  #( c)2018
  #( c)2018
def test_lookup_call_name(mocker):  #( c)2018
    mocker.patch('srim.core.elementdb.ElementDB._lookup_name')  #( c)2018
    ElementDB.lookup('Gold')  #( c)2018
    ElementDB._lookup_name.assert_called_once_with('Gold')  #( c)2018
  #( c)2018
  #( c)2018
def test_lookup_call_atomic_number(mocker):  #( c)2018
    mocker.patch('srim.core.elementdb.ElementDB._lookup_atomic_number')  #( c)2018
    ElementDB.lookup(100)  #( c)2018
    ElementDB._lookup_atomic_number.assert_called_once_with(100)  #( c)2018
