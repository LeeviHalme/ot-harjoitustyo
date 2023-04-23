# TKT20002 Ohjelmistotekniikka
Harjoitustyölle ja laskareille varattu git-repositorio.
<br />
This repository contains weekly excercises as well as the main project files for University of Helsinki's **TKT20002 Software Development Methods**.

## Budget Managing Application

Hallitse talouttasi tehokkaasti budjetointisovelluksen avulla. Voit lisätä henkilökohtaiseen budjettiisi koko kuukauden menot, tulot ja yllättävät kulut. Voit myös hallita useita budjetteja samalla käyttäjällä.

### Quick links
- [Requirements Specification](/dokumentaatio/VAATIMUSMAARITTELY.md)
- [Hourly Accounting](/dokumentaatio/TUNTIKIRJANPITO.md)
- [Changelog](/dokumentaatio/CHANGELOG.md)

### Local Setup
```sh
git clone git@github.com:LeeviHalme/ot-harjoitustyo.git
```
```
cd budget-manager
```
```
poetry install
```
```
poetry run invoke start
```