# Määrittelydokumentti
### Ohjelmointikielet
- Projektin kieli: **Python**
- Osaamani kielet: **Python**, **Javascript**, **C++** (vain perusteet)

## Projekti
Projektini on shakki pelimoottori. Projektissa on jo toimiva käyttöliittymä ja ohjelmistokoodi, mutta lähtötilanteessa, projektin peliäly on hyvin heikko.

Ongelma, jonka ratkaisen, on saada tästä peliälystä taidokkaampi, mielellään siten että peliäly ylittäisi ainakin 1500 elo pistettä (nykyinen peliäly on luultavasti 600 elo pisteen tienoilla). Projektiin joutuisi todennäköisesti rakentamaan lisäosan, jotta sen tulostukset olisivat yhteensopiva elo:n mittaus github projektien kanssa.

Projekti sisältää tällä hetkellä hyvin yksinkertaisen [minimax](https://www.chessprogramming.org/Minimax) algoritmin, [alpha-beta](https://www.chessprogramming.org/Alpha-Beta) karsinnan kera. Pisteet laudan tilanteille lasketaan vain nappien arvoista. Tämä peliäly, ja tarkemmin itse minimax algoritmi, olisi myös projektini ydin, jota lähtisin parantelemaan sekä itse algoritmia laajentaen, että laudan tilanteen pisteytystä tarkentaen.

Algoritmin voisi esimerkiksi laittaa tutkimaan syvemmin sellaisia polkuja, joista löytyy paljon nappien vaihtelua tai kuninkaan uhkauksia ([quiescence haku](https://www.chessprogramming.org/Quiescence_Search)). Voisin myös tallentaa tarkastettuja pöydän tilanteita myöhempää käyttöä varten ([transpositio taulu](https://www.chessprogramming.org/Transposition_Table)) ja siten parantaa suorituskykyä. Myös [null-move karsinta](https://www.chessprogramming.org/Null_Move_Pruning) ja etenkin [iterative deepening](https://www.chessprogramming.org/Iterative_Deepening) todennäköisesti kehittäisivät algoritmin suorituskykyä huomattavasti.

Itse laudan pisteytystä voisin parantaa muun muassa luomalla lämpökarttoja jokaiselle nappi tyypille sille parhaista ruuduista, joissa nappi hallitsisi mahdollisimman montaa muuta ruutua. Voisin myös esimerkiksi rangaista päällekkäisiä sotilaita ([doubled pawns](https://en.wikipedia.org/wiki/Doubled_pawns)) tai palkita tilanteita, joissa kuningas on suojattu.

Syötteenä peliäly saa pöydän tilanteen ja palauttaa uskomansa parhaimman liikkeen takaisin ohjelmalle. Syötettä käsitellään simuloimalla eri liikkeitä ja löytämällä parhaan liikkeen minimax algoritmin avulla.

Aikavaatimuksen suhteen, minimax algoritmin vaativuus on eksponentiaalinen, syvyyden kasvaessa. Kaikki aiemmat algoritmit joko keskittyvät suorituskyvyn parantamiseen tai resurssien keskittämiseen haaroihin, joista todennäköisemmin löytyy paras liike. Kuitenkin haun eksponentiaalisuuden takia on vaikeaa päästä muutamaa haaraa syvemmälle näilläkään keinoilla. Siksi on tärkeää keskittyä itse pöydän tilanteen pisteytyksen laatuun. Tilavaatimus puolestaan ei ole suuri ongelma sillä sen kasvu on lineaarista. Kuitenkin transpositio taulujen määrä voi silti kasvaa hyvinkin suureksi, solmujen myötä, joten sen määrää joutuu todennäköisesti rajoittamaan.

Lähteenä algoritmiparannuksille tulen käyttämään luultavasti hyvin paljon [shakkiohjelmointi wikiä](https://www.chessprogramming.org/Main_Page).


Opinto-ohjelmani on **tietojenkäsittelytieteen kandi**.