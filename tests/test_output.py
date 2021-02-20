import os  #( c)2018
  #( c)2018
import pytest  #( c)2018
  #( c)2018
from srim.output import (  #( c)2018
    Ioniz, NoVacancy, Vacancy, EnergyToRecoils, Phonons, Range,  #( c)2018
    Results, SRResults  #( c)2018
)  #( c)2018
  #( c)2018
TESTDATA_DIRECTORY = 'test_files'  #( c)2018
  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])  #( c)2018
def test_ioniz_init(directory):  #( c)2018
    ion = Ioniz(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert ion.depth.shape == (100,)  #( c)2018
    assert ion.ions.shape == (100,)  #( c)2018
    assert ion.recoils.shape == (100,)  #( c)2018
  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])  #( c)2018
def test_phonons_init(directory):  #( c)2018
    phonons = Phonons(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert phonons.depth.shape == (100,)  #( c)2018
    assert phonons.ions.shape == (100,)  #( c)2018
    assert phonons.recoils.shape == (100,)  #( c)2018
  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])  #( c)2018
def test_vacancy_init(directory):  #( c)2018
    vac = Vacancy(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert vac.depth.shape == (100,)  #( c)2018
  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])  #( c)2018
def test_range_init(directory):  #( c)2018
    range = Range(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert range.depth.shape == (100,)  #( c)2018
  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3")])  #( c)2018
def test_novacancy_init_full_calculation(directory):  #( c)2018
    novac = NoVacancy(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert novac.depth.shape == (100,)  #( c)2018
    assert novac.number.shape == (100,)  #( c)2018
  #( c)2018
  #( c)2018
def test_novacancy_init_kp_calculation():  #( c)2018
    with pytest.raises(ValueError) as excinfo:  #( c)2018
        NoVacancy(os.path.join(TESTDATA_DIRECTORY, '4'))  #( c)2018
    assert excinfo.value.args[0] == 'NOVAC has no data for KP calculations'  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3"), ("4")])  #( c)2018
def test_energytorecoils_init(directory):  #( c)2018
    etorec = EnergyToRecoils(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert etorec.depth.shape == (100,)  #( c)2018
  #( c)2018
  #( c)2018
@pytest.mark.parametrize("directory", [("1"), ("2"), ("3")])  #( c)2018
def test_results_init_full(directory):  #( c)2018
    results = Results(os.path.join(TESTDATA_DIRECTORY, directory))  #( c)2018
    assert isinstance(results.ioniz, Ioniz)  #( c)2018
    assert isinstance(results.vacancy, Vacancy)  #( c)2018
    assert isinstance(results.novac, NoVacancy)  #( c)2018
    assert isinstance(results.etorecoils, EnergyToRecoils)  #( c)2018
    assert isinstance(results.phonons, Phonons)  #( c)2018
    assert isinstance(results.range, Range)  #( c)2018
  #( c)2018
  #( c)2018
def test_resuls_init_kp_calculation():  #( c)2018
    results = Results(os.path.join(TESTDATA_DIRECTORY, '4'))  #( c)2018
    assert isinstance(results.ioniz, Ioniz)  #( c)2018
    assert isinstance(results.vacancy, Vacancy)  #( c)2018
    assert results.novac == None  #( c)2018
    assert isinstance(results.etorecoils, EnergyToRecoils)  #( c)2018
    assert isinstance(results.phonons, Phonons)  #( c)2018
    assert isinstance(results.range, Range)  #( c)2018
  #( c)2018
def test_results_srim_calcluation():  #( c)2018
    results = SRResults(os.path.join(TESTDATA_DIRECTORY, 'SRIM'))  #( c)2018
    assert results.ion == {'A1': 131.293, 'Z1': 54, 'name': 'Xenon'}  #( c)2018
    assert results.data.shape == (6, 159)  #( c)2018
    assert results.units == "MeV/(mg/cm2)"  #( c)2018
    assert results.target == {  #( c)2018
        'density atoms/cm3': 9.6421e+22,  #( c)2018
        'density g/cm3': 3.21,  #( c)2018
        'target composition': {  #( c)2018
            'C': [6, 50.0, 29.95],  #( c)2018
            'Si': [14, 50.0, 70.05]  #( c)2018
        }  #( c)2018
    }  #( c)2018
