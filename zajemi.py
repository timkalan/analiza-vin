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

    return vina_url



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
            vino['ocenjevalec'] = ocena['ocenjevalec']
        else:
            vino['ocena'] = None
            vino['ocenjevalec'] = None

    return vino



# vzorec za detajle s strani posameznega vina
vzorec_detajlov = re.compile(
    r'<meta property="og:url" content="https://winelibrary.com/wines.*?'
    r'<input type="hidden" name="product_id" value="(?P<id>\d{3,8})" />.*?'
    r"""Region.*?class="data"><a href=".*?">(?P<regija>.*?)</a></td>.*?"""
    r"""Sub-Region.*?class="data"><a href=".*?">(?P<podregija>.*?)</a></td>.*?"""
    r"""Color.*?class="data"><a href=".*?">(?P<barva>.*?)</a></td>.*?"""
    r"""ABV.*?class="data">(?P<alkohol>.*?)%?</td>.*?"""
    r"""Closure.*?class="data">(?P<zamasek>.*?)</td>.*?""",
    flags=re.DOTALL
)


vzorec_recenzije = re.compile(
    r"""<p itemprop='reviewBody'>"?(?P<recenzija>.*?)"?</p>""",
    flags=re.DOTALL
)


vzorec_opisa = re.compile(
    r"""<p itemprop='description'>"?(?P<opis>.*?)"?</p>""",
    flags=re.DOTALL
)


def izloci_detajle(stran):
    """
    Izloči vse relevantne podatke iz dejanske strani posameznega vina in 
    podatke malo olepša.
    """
    detajli = re.search(vzorec_detajlov, stran)
    if detajli:
        detajli = detajli.groupdict()
        recenzija = re.search(vzorec_recenzije, stran)
        opis = re.search(vzorec_opisa, stran)

        detajli['id'] = int(detajli['id'])
        if detajli['alkohol'] == 'N/A':
            detajli['alkohol'] = None
        else:
            detajli['alkohol'] = float(detajli['alkohol'])
        if detajli['zamasek'] == 'N/A':
            detajli['zamasek'] = None

        if opis:
            detajli['opis'] = opis['opis'].replace(
                '\n<br>\n<br>\n', ' ').replace(
                    '<br><br>\n\n', ' ').replace(
                        '\n<BR><BR>\n', ' ').replace(
                            '\n<br>\n', ' ').replace(
                                '\n', ' ')

        else:
            detajli['opis'] = None

        if recenzija:
            detajli['recenzija'] = recenzija['recenzija'].replace(
                '\n<br>\n', ' ').replace('\n', ' ')
        else:
            detajli['recenzija'] = None

    return detajli



vzorec_okusov = re.compile(
    r'<input type="hidden" name="product_id" value="(?P<id>\d{3,8})" />.*?'
    r'Taste</td>.*?class="data">(?P<okus>.*?)</td>',
    flags=re.DOTALL
)


vzorec_vonjav = re.compile(
    r'<input type="hidden" name="product_id" value="(?P<id>\d{3,8})" />.*?'
    r'Nose</td>.*?class="data">(?P<vonj>.*?)</td>',
    flags=re.DOTALL
)


def izloci_iz_seznama(vzorec, stran):
    """
    Za podatke o okusu in vonju, ki sta podana kot seznama izločimo in 
    shranimo posamezne kvalifikatorje. Vrne seznam slovarjev tipa 
    {id: kvalifikator}. 
    """
    if vzorec == vzorec_okusov:
        kljuc = 'okus'
    else:
        kljuc = 'vonj'
    
    kvalifikatorji = re.search(vzorec, stran)
    if kvalifikatorji:
        kvalifikatorji = kvalifikatorji.groupdict()
        kvalifikatorji['id'] = int(kvalifikatorji['id'])
        kvalifikatorji[kljuc] = kvalifikatorji[kljuc].replace(' and', ',')
        seznam = []
        for kvalifikator in kvalifikatorji[kljuc].replace(',', '').split():
            seznam.append(
                {
                    'id':kvalifikatorji['id'],
                    kljuc: kvalifikator
                }
            )
        return seznam



if __name__ == '__main__':
    zajemi_glavne()                     # shranimo glavne strani
    zajemi_posamezna(zajemi_glavne())   # shranimo posamezne strani

    # naredimo slovar iz glavnih strani
    slovarji_vin = []
    for vina in os.listdir('zajete_strani/vina'):
        for oglas in re.finditer(vzorec_oglasa, orodja.vsebina_datoteke(f'zajete_strani/vina/{vina}')):
            if izloci_podatke_vina(oglas.group(0)):
                slovarji_vin.append(izloci_podatke_vina(oglas.group(0)))

    # slovarji zi podstrani
    slovarji_detajlov = []
    slovarji_okusov = []
    slovarji_vonjav = []
    # upoštevamo, da so datoteke v večih direktorijih
    for direktorij in os.listdir('zajete_strani/oglasi'):
        if direktorij != '.DS_Store':
            for oglas in os.listdir(f'zajete_strani/oglasi/{direktorij}'):
                detajli = izloci_detajle(
                    orodja.vsebina_datoteke(f'zajete_strani/oglasi/{direktorij}/{oglas}'))

                if detajli:
                    detajli['popularnost'] = re.sub('[^0-9]', '', oglas)        # isluščimo zaporedno številko
                    slovarji_detajlov.append(detajli)  

                okusi = izloci_iz_seznama(
                    vzorec_okusov, orodja.vsebina_datoteke(f'zajete_strani/oglasi/{direktorij}/{oglas}'))
                vonjave = izloci_iz_seznama(
                    vzorec_vonjav, orodja.vsebina_datoteke(f'zajete_strani/oglasi/{direktorij}/{oglas}'))

                if okusi:
                    slovarji_okusov += okusi
                if vonjave:
                    slovarji_vonjav += vonjave

    
    # zapišemo CSV-je
    orodja.zapisi_csv(slovarji_vin, slovarji_vin[0].keys(), 'obdelani_podatki/vina.csv')
    orodja.zapisi_csv(
        slovarji_detajlov, 
        ['id', 'regija', 'podregija', 'barva', 'alkohol', 'zamasek', 'opis', 'recenzija', 'popularnost'], 
        'obdelani_podatki/detajli.csv')
    orodja.zapisi_csv(slovarji_okusov, ['id', 'okus'], 'obdelani_podatki/okusi.csv')
    orodja.zapisi_csv(slovarji_vonjav, ['id', 'vonj'], 'obdelani_podatki/vonjave.csv')
