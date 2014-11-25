__author__ = 'Giggiux'
import re

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

def soupify(siteStr):
    from bs4 import BeautifulSoup
    siteSoup = BeautifulSoup(siteStr)
    return siteSoup

def title(siteSoup):
    return siteSoup.title.string

def linkList(siteSoup):
    if siteSoup.find_all('a') == []:
        return ['']
    else:
        return siteSoup.find_all('a')

def linkDict(linkList):
    # lst = siteSoup.find_all('a')
    dictLink = dict()
    for link in linkList:
        if re.match('http://.*', str(link.get('href'))):
            dictLink[link.get('href')] = link.get_text()
            print(dictLink)
        else:
            continue

def showExternalLink(linkdict):
    for link in linkdict:
        print(str(link) + ' : ' + linkdict[link].strip())


# web = soupify(loadFromUrl('http://fmpassion.com'))
# web = soupify(loadFromFile('prova.html'))
# print(web.prettify())

def load():
    while True:
        choice = input('Do you want to analyze a file or an url? : ')
        if choice != 'file' and choice != 'url':
            print('ERROR: your choice is not valid. You can chose from \'file\' and \'url\'')
        elif choice == 'file':
            while True:
                try:
                    filepath = str(input('Please now insert the path to your page: '))
                    return soupify(loadFromFile(filepath))
                except:
                    print('There is an Error in the path!')
        else:
            while True:
                try:
                    urllink = str(input('Please now insert the url of your page: '))
                    return soupify(loadFromUrl(urllink))
                except:
                    print('There is an Error in the url!')

# web = load()
# print(type(web.prettify()))