import re
import orodja
import os


def zajemi_glavne(st_strani=99):
    """
    Zajame strani, kjer je seznam vin, hkrati za vsako vino poišče link na 
    njegovo unikatno stran in ga shrani v seznam.
    """
    vina_url = []
    vino_url_vzorec = re.compile(
        r'<a href=(?P<vino>"https://winelibrary.com/(wines|others|gourmet)/.*?)><img', 
                    re.DOTALL)

    for i in range(st_strani):
        # shranimo strani v unikatne datoteke
        orodja.shrani_spletno_stran(f'https://winelibrary.com/search?page={i}&search=', 
                                    f'zajete_strani/vina/vina{i * 25 + 1}-{(i+1) * 25}.html')
        vina_url += re.findall(
            vino_url_vzorec, orodja.vsebina_datoteke(
                f'zajete_strani/vina/vina{i * 25 + 1}-{(i+1) * 25}.html'))

        print(len(vina_url))
    print(vina_url[0])
    return vina_url


# naštimi to da ti da v tri folderje da github pobere
def zajemi_posamezna(seznam_urljev):
    """
    Od zgornje funkcije prejme seznam vin in pobere njih posamezne strani. Hkrati 
    dobi tudi vrsto proizvoda - ni nujno, da so samo vina.
    """
    i = 1
    for link, vrsta in seznam_urljev:

        if i <= 1000:
            orodja.shrani_spletno_stran(link[1:-1], f'zajete_strani/oglasi/01/oglas{i}.html')

        elif (i >= 1001) and (i <= 2000):
            orodja.shrani_spletno_stran(link[1:-1], f'zajete_strani/oglasi/02/oglas{i}.html')

        else:
            orodja.shrani_spletno_stran(link[1:-1], f'zajete_strani/oglasi/03/oglas{i}.html')

        i += 1


# vzorec enega od 25 oglasov na strani
vzorec_oglasa = re.compile(
    r'<div id="product_id.*?' 
    r'<div class="clearfix"></div>',
    flags=re.DOTALL
)

# vzorec oglasa, ki predstavlja vino (gourmet in other spustimo)
vzorec_vina = re.compile(
    r'<div id="product_id_(?P<id>\d{3,8}).*?'
    r'<a href="https://winelibrary.com/wines.*?'
    r"<span class='js-elip-multi'>(?P<leto>\d{4})? "
    r'(?P<ime>.*?)</span>.*?'
    r'<small>(?P<sorta>.*?) from '
    r'(?P<drzava>.*?)</small>.*?'
    r'</small> &nbsp; (<small>)?(?P<velikost>\d{1,4}).*?(</small>)?</p>.*?'
    r'<p class="h4 search-item-price">.*?\$(?P<znizana_cena>\d{1,5}\.\d{0,2}).*?'
    r"<span class='strike'>\$(?P<cena>\d{1,5}\.\d{0,2})</span>", 
    flags=re.DOTALL
)


# vzorec ocene in ocenjevalca (ni nujno, da se pojavita)
vzorec_ocene = re.compile(
    r'<div><span class="ptag-score">(?P<ocena>\d{2}).*?</span>.*?'
    r'<span class="name">(?P<ocenjevalec>.*?)</span>.*?', 
    flags=re.DOTALL
)


def izloci_podatke_vina(oglas):
    """
    Izloči vse relevantne podatke iz enega od 25 oglasov, ki so na vsaki strani. 

    oglas = del HTML-ja, ki predstavlja en oglas
    """
    vino = re.search(vzorec_vina, oglas)
    if vino:
        vino = vino.groupdict()
        ocena = re.search(vzorec_ocene, oglas)

        vino['id'] = int(vino['id'])
        if vino['leto']:
            vino['leto'] = int(vino['leto'])
        vino['velikost'] = int(vino['velikost'])
        vino['cena'] = float(vino['cena'])
        vino['znizana_cena'] = float(vino['znizana_cena'])

        if vino['leto']:
            vino['leto'] = int(vino['leto'])

        if ocena:
            vino['ocena'] = int(ocena['ocena'])
            vino['ocenjevaletc'] = ocena['ocenjevalec']
        else:
            vino['ocena'] = None
            vino['ocenjevalec'] = None

    return vino



vzorec_detajlov = re.compile(
    r'<input type="hidden" name="product_id" value="(?P<id>\d{3,8})" />.*?'
    r"""Region.*?class="data"><a href=".*?">(?P<regija>.*?)</a></td>.*?"""
    r"""Sub-Region.*?class="data"><a href=".*?">(?P<podregija>.*?)</a></td>.*?"""
    r"""Color.*?class="data"><a href=".*?">(?P<barva>.*?)</a></td>.*?"""
    r"""ABV.*?class="data">(?P<alkohol>.*?)%</td>.*?"""
    #r"""Varietal(s).*?class="data"><a href=".*?">(?P<varietal>.*?)</a>.*?""",
    r"""Closure.*?class="data">(?P<zamasek>.*?)</td>.*?""",
    flags=re.DOTALL
)


vzorec_recenzije = re.compile(
    r"""<p itemprop='reviewBody'>"(?P<recenzija>.*?)"</p>""",
    flags=re.DOTALL
)


vzorec_opisa = re.compile(
    r"<p itemprop='description'>(?P<opis>.*?)</p>",
    flags=re.DOTALL
)


def izloci_detajle(stran):
    """
    Izloči vse relevantne podatke iz dejanske strani posameznega vina.
    """
    detajli = re.search(vzorec_detajlov, stran).groupdict()
    recenzija = re.search(vzorec_recenzije, stran)
    opis = re.search(vzorec_opisa, stran)

    detajli['id'] = int(detajli['id'])
    detajli['alkohol'] = float(detajli['alkohol'])

    if opis:
        detajli['opis'] = opis['opis'].replace('\n<br>\n<br>\n', ' ').replace('<br><br>\n\n', ' ')
    else:
        detajli['opis'] = None

    if recenzija:
        detajli['recenzija'] = recenzija['recenzija']
    else:
        detajli['recenzija'] = None

    return detajli



vzorec_okusov = re.compile(
    r'<input type="hidden" name="product_id" value="(?P<id>\d{3,8})" />.*?'
    r'Taste.*?class="data">(?P<okusi>.*?)</td>',
    flags=re.DOTALL
)


vzorec_vonjav = re.compile(
    r'<input type="hidden" name="product_id" value="(?P<id>\d{3,8})" />.*?'
    r'Nose.*?class="data">(?P<vonjave>.*?)</td>',
    flags=re.DOTALL
)


def izloci_iz_seznama(vzorec, stran):
    """
    Za podatke o okusu in vonju, ki sta podana kot seznama izločimo in 
    shranimo posamezne kvalifikatorje. Vrne seznam slovarjev tipa 
    id: kvalifikator 
    """
    if vzorec == vzorec_okusov:
        kljuc = 'okusi'
    else:
        kljuc = 'vonjave'
    
    kvalifikatorji = re.search(vzorec, stran).groupdict()
    kvalifikatorji['id'] = int(kvalifikatorji['id'])
    kvalifikatorji[kljuc] = kvalifikatorji[kljuc].replace(' and', ',')
    seznam = []
    for kvallifikator in kvalifikatorji[kljuc].replace(',', '').split():
        seznam.append(
            {
                kvalifikatorji['id']: kvallifikator
            }
        )
    return seznam




def shrani_in_preglej_oglas():
    pass


def shrani_in_preglej_vina():
    pass



if __name__ == '__main__':
    #zajemi_glavne()                     # shranimo glavne strani
    #zajemi_posamezna(zajemi_glavne())   # shranimo posamezne strani

    #slovarji_vin = []
    #for vina in os.listdir('zajete_strani/vina'):
    #    for oglas in re.finditer(vzorec_oglasa, orodja.vsebina_datoteke(f'zajete_strani/vina/{vina}')):
    #        slovarji_vin.append(izloci_podatke_vina(oglas.group(0)))

    slovarji_detajlov = []
    for direktorij in os.listdir('zajete_strani/oglasi'):
        for oglas in os.listdir(f'zajete_strani/oglasi/{direktorij}'):
            print(izloci_detajle(orodja.vsebina_datoteke(f'zajete_strani/oglasi/{direktorij}/{oglas}')))
            slovarji_detajlov.append(izloci_detajle(orodja.vsebina_datoteke(f'zajete_strani/oglasi/{direktorij}/{oglas}')))
            break
        break




#for oglas in re.finditer(vzorec_oglasa, orodja.vsebina_datoteke('zajete_strani/vina/vina1-25.html')):
#    print(izloci_podatke_vina(oglas.group(0)))


#print(izloci_iz_seznama(vzorec_vonjav, orodja.vsebina_datoteke('zajete_strani/oglasi/01/oglas5.html')))



# TODO: odloči se, če boš zajemal tudi other in gourmet
# TODO: a bodo varietals zajeti