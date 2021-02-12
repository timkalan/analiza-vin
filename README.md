# Analiza vin

V sklopu predmeta Programiranje 1 bom analiziral 2467 vin, podatki o njih so zajeti s strani 
[Wine Library](https://winelibrary.com/search?page=1&search=). Število vin se rahlo spreminja, 
jaz bom delal s stranjo, zajeto 22.10.2020 ob 14:00

Za vsako vino bom zajel:
* ime vina
* zaporedna številka (id) vina
* sorta vina
* država izvora
* leto ustekleničenja
* prostornina buteljke
* položaj na lestvici popularnosti
* ocena profesionalca
* cena (in popust)
* opis
* kratka recenzija
* regija in podregija
* barva 
* procent alkohola
* način zapiranja buteljke
* okus in vonj

Delovne hipoteze in vprašanja:
* Najboljša vina so daleč od najbolj popularnih
* 750ml je najbolj popularna in najbolje ocenjena velikost buteljke
* Katero leto je bilo najboljše za vino?
* Katera država je "najboljša", kar se tiče vin?
* Katera je najbolj popularna sorta?
* Katere so najboljše regije?
* Kateri okusi in vonjave so najbolj priljubljeni?
* Ljudje preferirajo belo vino


## Podatki
Podatki so urejeni v štiri `.csv` datoteke, ki jih dobimo, ko poženemo `zajemi.py`:
* `vina.csv` vsebuje stolpce: id, leto, ime, sorta, drzava, velikost, znizana_cena, 
    cena, ocena, ocenjevalec
* `detajli.csv` vsebuje stolpce: id, regija, podregija, barva, alkohol, zamasek, 
    opis, recenzija, popularnost 
* `okusi.csv` vsebuje stolpca: id, okus
* `vonjave.csv` vsebuje stolpca: id, vonj


## Navodila
Da podatke pridobimo, enostavno poženemo `zajemi.py`, ki generira vse štiri `.csv` 
datoteke v mapi `obdelani_podatki`. 

V mapi `zajete_strani` se nahajajo vnaprej shranjene `.html` datoteke, ki jih je 
kar precej, zato priporočamo, da se shrani tudi ta mapa. Tako se doseže najvišja 
konsistenca z analizo in najmanjši promet na spletni strani. 

Analiza podatkov se nahaja v zvezku `vina.ipynb`.