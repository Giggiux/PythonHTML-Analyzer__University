__author__ = 'Giggiux'


def loadFromUrl(page):
    # while True:
    #     try:
    import urllib.request
    siteStr = urllib.request.urlopen(page).read().decode('utf-8')
    return siteStr
        # except:
        #     print('The url is not valid')
# loadFromUrl('http://fmpassion.com')

def loadFromFile(page):
    siteStr = open(page, 'r').read()
    return siteStr
# loadFromFile('prova.html')

def soupify(site):
    from bs4 import BeautifulSoup
    web = BeautifulSoup(site)
    return web

# web = soupify(loadFromUrl('http://fmpassion.com'))
# web = soupify(loadFromFile('prova.html'))
# print(web.prettify())

