# Changelog

## Viikko 3
- Projektiin lisätty ja kofiguroitu poetry, invoke ja tkinter
  - Lisätty myös invoke-komennot:
    - `poetry run invoke start`
    - `poetry run invoke test`
    - `poetry run invoke coverage-report`
- Lisätty ensimmäinen käyttöliittymänäkymä: *Kirjaudu sisään*
- Päätetty kansiorakenteesta seuraavaa: näkymät sijoitetaan kansion `views/` alle
- Ei vielä testejä kirjoitettuna, koska ei ole mielekästä testata käyttöliittymäluokkia. Tulevilla viikoilla lisätään sovelluslogiikkaa, joille voi kirjoittaa jo testejä.