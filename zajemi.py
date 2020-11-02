import re
import orodja


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
        orodja.shrani_spletno_stran(link[1:-1], f'zajete_strani/oglasi/oglas{i}.html')
        i += 1
        print(i)


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
    r'<div><span class="ptag-score">(?P<ocena>.*?)</span>.*?'
    r'<span class="name">(?P<ocenjevalec>.*?)</span>.*?', 
    flags=re.DOTALL
)

#vzorec_other = re.compile(
#    r'', 
#    flags=re.DOTALL
#)
#
#
#vzorec_gourmet = re.compile(
#    r'', 
#    flags=re.DOTALL
#)


def izloci_podatke_oglasa(oglas):
    """
    Izloči vse relevantne podatke iz enega od 25 oglasov, ki so na vsaki strani. 

    oglas = del HTML-ja, ki predstavlja en oglas
    """

i = 0
for oglas in re.finditer(vzorec_oglasa, orodja.vsebina_datoteke('zajete_strani/vina/vina101-125.html')):
    if re.search(vzorec_ocene, oglas[0]):
        print(re.search(vzorec_ocene, oglas[0]).groupdict())
        i += 1

print(i) 