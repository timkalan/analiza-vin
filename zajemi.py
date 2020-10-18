import re
import orodja

url = 'https://winelibrary.com/search?page=1&search='

for i in range(1, 99):
    orodja.shrani_spletno_stran(f'https://winelibrary.com/search?page={i}&search=', 
                                f'zajete_strani/vina{i}.html')