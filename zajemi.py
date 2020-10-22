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


if __name__ == '__main__':
    #zajemi_glavne()
    #zajemi_posamezna(zajemi_glavne())
    print(zajemi_glavne()[-1])