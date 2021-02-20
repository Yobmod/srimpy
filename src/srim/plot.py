def plot_damage_energy(results, ax):  #( c)2018
    """Plot damage energy (ions + recoils) per unit depth  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    results : :class:`srim.output.Results`  #( c)2018
        results from srim calcualtion  #( c)2018
    ax : matplotlib.Axes  #( c)2018
        matplotlib axes to plot into  #( c)2018
    """  #( c)2018
    phon = results['phonons']  #( c)2018
    dx = max(phon.depth) / 100.0 # to units of Angstroms  #( c)2018
    energy_damage = (phon.ions + phon.recoils) * dx  #( c)2018
    ax.plot(phon.depth, energy_damage / phon.num_ions, label='{}'.format(folder))  #( c)2018
    return sum(energy_damage)  #( c)2018
  #( c)2018
  #( c)2018
def plot_ionization(results, ax):  #( c)2018
    """Plot ionization (ion vs recoils) per unit depth  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    results : :class:`srim.output.Results`  #( c)2018
        results from srim calcualtion  #( c)2018
    ax : matplotlib.Axes  #( c)2018
        matplotlib axes to plot into  #( c)2018
    """  #( c)2018
    ioniz = results['ioniz']  #( c)2018
    dx = max(ioniz.depth) / 100.0 # to units of Angstroms  #( c)2018
    ax.plot(ioniz.depth, ioniz.ions, label='Ionization from Ions')  #( c)2018
    ax.plot(ioniz.depth, ioniz.recoils, label='Ionization from Recoils')  #( c)2018
  #( c)2018
  #( c)2018
def plot_vacancies(results, ax):  #( c)2018
    """Plot vacancies (ion + recoils produced) per unit depth  #( c)2018
  #( c)2018
    Parameters  #( c)2018
    ----------  #( c)2018
    results : :class:`srim.output.Results`  #( c)2018
        results from srim calcualtion  #( c)2018
    ax : matplotlib.Axes  #( c)2018
        matplotlib axes to plot into  #( c)2018
    """  #( c)2018
    vac = results['vacancy']  #( c)2018
    vacancy_depth = vac.knock_ons + np.sum(vac.vacancies, axis=1)  #( c)2018
    ax.plot(vac.depth, vacancy_depth, label="Total vacancies at depth")  #( c)2018
    return sum(vacancy_depth)  #( c)2018
