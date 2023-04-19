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

## Viikko 4
- Aloitettu sovelluksen toiminnallisuudet:
  - Tietokantayhteys SQLite-tietokantaan
  - Sovelluslogiikka, sekä käyttöliittymälogiikka autentikoinnille
    - Lisätty uusi käyttöliittymänäkymä *Rekisteröidy*
    - Refaktoroitu sovellus käyttämään repositorio-suunnittelumallia