# Tehtävä 1: Monopoli

```mermaid
classDiagram
  Lauta "1" --> "2-8" Pelaaja
  Pelaaja "1" --> "1" Nappula
  Lauta "1" --> "2" Noppa
  Lauta "1" <--> "40" Ruutu
  Nappula "1" --> "1" Ruutu
  class Ruutu
  Ruutu : +Ruutu seuraava
```