import requests
import re
import os

save_dir = 'cache'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def fetch(url):
    x = requests.get(
        url
    )
    return x.text

# To keep from hammering the website, this caches each request
def cache_fetch(url):
    ext = '.html'
    name = re.sub(r'\W+', '', url) # FIXME? Dollar store hashing

    fname = name + ext

    found = False
    for f in os.listdir(save_dir): # FIXME slow, no short circuiting
        if fname == f.__str__():
            found = True

    furi = f'{save_dir}/{fname}'
    if found:
        with open(furi, 'r', encoding='utf-8') as g: # FIXME test this on windows
            return g.read()
    else:
        print("FETCHING")
        html = fetch(url)

        with open(furi, 'w', encoding='utf-8') as g:
            g.write(html)


        return html

