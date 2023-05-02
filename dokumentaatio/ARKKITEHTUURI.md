# Sovelluksen arkkitehtuurikuvaus
Rakenteessa noudatetaan kaksitasoista kerrosarkkitehtuuria ja sovelluksen pakkausrakenne on seuraava:
![pakkausrakenne](images/package_diagram.png)


## Hakemistojen kuvaukset
- `data`- Sisältää tietokantaan liittyvät tiedostot
- `src`- Sisältää sovelluksen lähdekoodin
  - `entities`- Sisältää yleisesti käytettyjä olioita, jotka kuvastavat sovelluksen tietorakenteita
  - `repositories`- Sisältää repositoriot, joiden kautta käyttöliittymä muokkaa ja hakee dataa 
  - `tests`- Sisältää sovelluksen automaattiset yksikkötestit
  - `utils`- Sisältää "apuvälineitä" eli metodeja joita käytetään useasti ja monesta moduulista
  - `views`- Sisältää käyttöliittymänäkymät

## Päätoiminnallisuudet

Kuvataan seuraavaksi sovelluksen toimintalogiikka muutaman päätoiminnallisuuden osalta sekvenssikaaviona.

### Käyttäjän sisäänkirjautuminen
Kun *Kirjaudu*-näkymän syötekenttiin kirjoitetaan tietokannassa oleva käyttäjätunnus ja salasana ja painetaan "Kirjaudu", etenee kontrolli seuraavasti:
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant AuthRepository
  participant UserRepository
  participant utils
  participant entities
  User->>UI: enter details and click "Login" button
  UI->>AuthRepository: login_using_username_pass("kalle", "kalle123")
  AuthRepository->>UserRepository: get_by_username("kalle")
  UserRepository->>utils:get_database_connection()
  utils-->>UserRepository: connection
  note over UserRepository: query user data from SQLite
  UserRepository-->>AuthRepository: {"id": "2ad70b...", "name": "Kalle", "username": "kalle"}
  note over AuthRepository: validate password hashes
  AuthRepository->>entities: create new user entity
  entities-->>AuthRepository: User("2ad70b...", "Kalle", "kalle")
  note over AuthRepository: store user session in state
  AuthRepository-->>UI: True
  UI->UI: budgets_view()
  UI-->>User: see budgets view
```

Jos käyttäjätunnus tai salasana ovat väärin, sovellus palauttaa käyttäjäystävällisen virheviestin.

### Käyttäjän rekisteröinti
Kun *Rekisteröidy*-näkymän syötekenttiin kirjoitetaan uniikin käyttäjän tiedot ja painetaan "Rekisteröidy", etenee kontrolli seuraavasti:
```mermaid
sequenceDiagram
  actor User
  participant UI
  participant AuthRepository
  participant UserRepository
  participant utils
  participant entities
  User->>UI: enter details and click "Register" button
  note over UI: validate input
  UI->>AuthRepository: register_new_user("Kalle", "kalle", "kalle123")
  AuthRepository->>UserRepository: get_by_username("kalle")
  UserRepository->>utils:get_database_connection()
  utils-->>UserRepository: connection
  note over UserRepository: query user data from SQLite
  UserRepository-->AuthRepository: None
  note over AuthRepository: hash user password
  AuthRepository->>UserRepository: create_new_user("Kalle", "kalle", hash)
  AuthRepository->>UserRepository: get_by_username("kalle")
  UserRepository-->>AuthRepository: {"id": "2ad70b...", "name": "Kalle", "username": "kalle"}
  AuthRepository->>entities: create new user entity
  entities-->>AuthRepository: User("2ad70b...", "Kalle", "kalle")
  note over AuthRepository: store user session in state
  AuthRepository-->>UI: True
  UI->UI: budgets_view()
  UI-->>User: see budgets view
```

Jos käyttäjätunnus on olemassa tai salasana ja sen vahvistus eivät täsmää, sovellus palauttaa käyttäjäystävällisen virheviestin.

## Ohjelman rakenteeseen jääneet heikkoudet

Tällä hetkellä sovelluksella ei ole käytössä ns. service-luokkia, vaan esimerkiksi syötteen validointi tapahtuu käyttöliittymässä. Tällä ei kuitenkaan ole mielestäni suurta haittavaikutusta, sillä syötteet ovat pieniä ja tietokannan skeema on asianmukaisesti konfiguroitu väärien syötteiden varalta.