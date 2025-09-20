# Viikkoraportti

Tällä viikolla parantelin tekoälyä ja sitä tukevaa koodia (kuten liikkeen generointia ja pelilaudan tietorakennetta), laajensin tekoälyn testausta ja koitin saada arvioitua shakkipeliälyn Elo-lukua. Yritin arvioida projektin tasoa laittamalla sen Stockfish-tekoälyä vastaan Cutechess-projektin avulla. Tämän vuoksi jouduin koodaamaan projektiin wrapperin Universal Chess Interface -protokollalle. Lopulta en saanut Cutechess-projektia toimimaan oman projektini kanssa, joten päätin ainakin toistaiseksi jättää Elo-arvioinnin taka-alalle, sillä sen tukeminen veisi liikaa aikaa itse tekoälyn kehittämiseltä. Jos projektin loppupuolella jää aikaa, voin Git-historian avulla palata vertaamaan aiempaa peliälyä sen hetkiseen versioon.

Opin paljon tällä viikolla. Tekoälyn testaus paljasti puutteita shakkimattien pakottamisessa, ja opin lisää matalan ja syvän tason kopioinnin eroista. Kuten aiemmin mainitsin, opin myös kuinka haastavaa Elo-lukujen arviointi tulisi olemaan näin erikoisen shakkimoottorin kanssa. Epäselvyyksiä syntyi enimmäkseen Cutechess-projektin kanssa, sekä sen selvittämisessä, miksi tekoäly ei suorita laskentasyvyyden sisällä olevia pakotettuja shakkimatteja. Uskon kuitenkin, että saan nämä ongelmat ratkaistua itse.

Testikattavuuden selvittämiseen löytyivät jo aiemmalla kurssilla laatimani työkalut.

Seuraavaksi jatkan tekoälyn debuggausta sekä sitä tukevan koodin parantelua. Näiden jälkeen siirryn heuristiikan tarkentamiseen.

---
Tunteja käytetty: 19