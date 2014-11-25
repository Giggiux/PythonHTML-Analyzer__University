__author__ = 'Giggiux'
import re
mainTagList = ['div','a','table','h1','h2','h3','p','img']
mainTagDict = {'div':'divisors','a':'links','table':'tables','h1':'h1 headers','h2':'h2 headers','h3':'h3 headers','p':'paragraphs','img':'images'}

# LOADING FUNCTIONS
def loadFromUrl(page):
    import urllib.request
    siteStr = urllib.request.urlopen(page).read().decode('utf-8')
    return siteStr

def loadFromFile(page):
    siteStr = open(page, 'r').read()
    return siteStr

def soupify(siteStr):
    from bs4 import BeautifulSoup
    siteSoup = BeautifulSoup(siteStr)
    return siteSoup

# BASIC FUNCTIONS
def makeTitle(siteSoup):
    return siteSoup.title.string

def countMainTags(siteSoup):
    global mainTagList
    global mainTagDict
    countDict = dict()
    for tag in mainTagList:
        listTag = siteSoup.find_all(tag)
        countDict[mainTagDict[tag]] = str(len(listTag))
    return countDict

# ADVANCED FUNCTIONS
def linkList(siteSoup):
    if siteSoup.find_all('a') == []:
        return ['']
    else:
        return siteSoup.find_all('a')

def linkDict(linkList):
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

def countOtherTags(siteSoup):
    global mainTagList
    countDict = dict()
    for tag in siteSoup.body.find_all(True):
        if tag.name not in mainTagList and tag.name not in countDict:
            listTag = siteSoup.find_all(tag.name)
            countDict[tag.name] = str(len(listTag))
    return countDict

# MAIN FUNCTIONS
def load():
    while True:
        choice = input('Do you want to analyze a file, an url or you want to quit? : ')
        if choice != 'file' and choice != 'url' and choice != 'quit':
            print('ERROR: your choice is not valid. You can chose from \'file\' and \'url\'')
        elif choice == 'file':
            while True:
                try:
                    filepath = str(input('Please now insert the path to your page: '))
                    return soupify(loadFromFile(filepath))
                except:
                    print('There is an Error in the path!')
        elif choice == 'url':
            while True:
                try:
                    urllink = str(input('Please now insert the url of your page: '))
                    return soupify(loadFromUrl(urllink))
                except:
                    print('There is an Error in the url!')
        else:
            exit()

def header():
    title = makeTitle(site)
    maintagsDict = countMainTags(site)
    print('Page Title is \'' + str(title) + '\'')
    print('This page has:')
    for key in maintagsDict:
        if maintagsDict[key] != '0':
            print('\'' + maintagsDict[key], key + '\'', '\t', end='')

def advanced():
    while True:
        request = input('Do you want ')



def main():
    header()

site = load()
main()
# print(countOtherTags(site))
# print(title(site))
# print(countMainTags(site))