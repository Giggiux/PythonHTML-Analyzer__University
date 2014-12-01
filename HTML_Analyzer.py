__author__ = 'Giggiux'
import re
mainTagDict = {'div':'divisors','a':'links','table':'tables','h1':'h1 headers','h2':'h2 headers','h3':'h3 headers','p':'paragraphs','img':'images'} #This is for the main tags and their formal names

temporaryTxt = [] #For the temporary output file


# LOADING FUNCTIONS
def loadFromUrl(page): #Function that load the page from an url
    import urllib.request
    try:
        siteStr = urllib.request.urlopen(page).read().decode('utf-8') #Read the html of the site and decode it
        return siteStr
    except UnicodeDecodeError:
        siteStr = urllib.request.urlopen(page).read() #Read the html of the site only
        return siteStr

def loadFromFile(page): #Function that load the page from a file
    siteStr = open(page, 'r').read() #Read the file
    return siteStr

def soupify(siteStr): #Function that takes the string loaded from a file or an url and change it in the bs4.BeautifulSoup type.
    from bs4 import BeautifulSoup
    siteSoup = BeautifulSoup(siteStr)
    return siteSoup

# BASIC FUNCTIONS
def makeTitle(): #Function that return the title, it works only if the site is previously loaded from the load() function
    global site
    return site.title.string #return it like a string

def countMainTags(siteSoup): #Function that simply count the main tags (that in the dictionary)
    global mainTagDict
    countDict = dict()
    for tag in mainTagDict:
        listTag = siteSoup.find_all(tag) #This bs4 command return a list with all the 'tag' codes
        countDict[mainTagDict[tag]] = str(len(listTag)) #add the tag as a key and count it with the len of the list
    return countDict

# ADVANCED FUNCTIONS
def linkList(siteSoup):     #Function that return a list with all the contents of the 'a' tag
    if siteSoup.find_all('a') == []:
        return ['']
    else:
        return siteSoup.find_all('a')

def linkDict(linkList): #Function that takes the list from linkList and create a dictionary only with external links
    dictLink = dict()
    for link in linkList:
        if re.match('http+(s)?://.*', str(link.get('href'))): #only if the link starts with http:// or https://
            dictLink[link.get('href')] = link.get_text()
        else:
            continue
    return dictLink

def showExternalLink(linkdict): #Print and saves in the temporary list the external links ad the 'linked' text
    global temporaryTxt
    for link in linkdict:
        linkDescription = linkdict[link].strip()
        linkDescriptionNew = ''.join(e for e in linkDescription if e != '\n')
        temporaryTxt.append(str(link) + ' : ' + linkDescriptionNew + '\n')
        print(str(link) + ' : ' + linkDescriptionNew + '\n')
        
def countOtherTags(siteSoup): #Function that count all the tags that are not main
    global mainTagDict
    countDict = dict()
    for tag in siteSoup.body.find_all(True): #Show all the tags content
        if tag.name not in mainTagDict and tag.name not in countDict: #If only the name of the tag (so not all the content) is not main counts it in the same wai of countMainTags()
            listTag = siteSoup.find_all(tag.name)
            countDict[tag.name] = str(len(listTag))
    return countDict

def showOtherTags(site): #Show all the tag that are not main and how many times they are repeated
    global temporaryTxt
    otherTagsDict = countOtherTags(site)
    for key in otherTagsDict:
        if otherTagsDict[key] != '0':
            temporaryTxt.append('\'' + otherTagsDict[key] + ' ' + key + '\'' + '\t')
            print('\'' + otherTagsDict[key], key + '\'', '\t', end='')

def linkDictValidate(linkList): #Create a dictionary with all the links
    dictLink = dict()
    for link in linkList:
        # if re.match('http://.*', str(link.get('href'))):
        dictLink[link.get('href')] = link.get_text() #takes only the 'href' attribute of the <a> tag
        # else:
        #     continue
    return dictLink

def validateLink(linkdict): #Function that tryes to open all the links for seeing it is valid or invalid
    global temporaryTxt
    import urllib.request
    global path
    for link in linkdict:
        if re.match('http+(s)?://.*', link): #Only if starts with http or https
            try:
                urllib.request.urlopen(link)
                temporaryTxt.append(str(link) + '\t\t : The link is valid' + '\n')
                print(str(link) + '\t\t : The link is valid')
            except:
                temporaryTxt.append(str(link) + '\t\t : The link is invalid' + '\n')
                print(str(link) + '\t\t : The link is invalid')
        elif re.match('#.*', link): #if it is an internal link add the site path before
            try:
                newLink = path + link
                urllib.request.urlopen(newLink)
                temporaryTxt.append(str(newLink) + '\t\t : The link is valid' + '\n')
                print(str(newLink) + '\t\t : The link is valid')
            except:
                temporaryTxt.append(str(newLink) + '\t\t : The link is invalid' + '\n')
                print(str(newLink) + '\t\t : The link is invalid')
        elif re.match('mailto\:.*', link):
            continue
        else:
            try:
                newLink = path + '/' + link #if it is an internal link add the site path and / before
                urllib.request.urlopen(newLink)
                temporaryTxt.append(str(newLink) + '\t\t : The link is valid' + '\n')
                print(str(newLink) + '\t\t : The link is valid')
            except:
                temporaryTxt.append(str(newLink) + '\t\t : The link is invalid' + '\n')
                print(str(newLink) + '\t\t : The link is invalid')

def showTagContents(siteSoup): #asks if want to see the html contents of a particular tag
    global temporaryTxt
    tagList = []
    print('List of possible tag: ')
    for tag in siteSoup.body.find_all(True):
        if tag.name not in tagList:
            tagList.append(tag.name)
            print(tag.name + '\t', end='')
    choice = 'something that is not a tag'
    while choice not in tagList:
        choice = input('\n What tag do you want to analyze? : ')
        if choice not in tagList:
            print('Wrong input, please retry!')
        else:
            contentList = siteSoup.body.find_all(choice)
            for content in range(len(contentList)):
                temporaryTxt.append('########### The #' + str(content) + '\'' + choice + '\' contains: ###########\n' + str(contentList[content]) + '\n' + '\n')
                print('########### The #' + str(content) + '\'' + choice + '\' contains: ###########\n' + str(contentList[content]) + '\n')
            return False

def goodbye(): #... Goodbye!
    print('Goodbye!')
    exit()

# MAIN FUNCTIONS
def load(): #Try to load the file and if something goes wrong re-ask to the user the input
    global path
    while True:
        choice = input('Do you want to analyze a file, an url or you want to quit? : ')
        if choice != 'file' and choice != 'url' and choice != 'quit':
            print('ERROR: your choice is not valid. You can chose from \'file\' and \'url\'')
        elif choice == 'file':
            while True:
                try:
                    filepath = str(input('Please now insert the path to your page: '))
                    path = filepath
                    return soupify(loadFromFile(filepath))
                except:
                    print('There is an Error in the path!')
        elif choice == 'url':
            while True:
                try:
                    urllink = str(input('Please now insert the url of your page: '))
                    path = urllink
                    return soupify(loadFromUrl(urllink))
                except:
                    print('There is an Error in the url!')
        else:
            goodbye()

def header(): #simply print the Header of the program
    global temporaryTxt
    global site
    title = makeTitle()
    maintagsDict = countMainTags(site)
    temporaryTxt.append('Page Title is \'' + str(title) + '\'' + '\n')
    print('Page Title is \'' + str(title) + '\'')
    temporaryTxt.append('This page has:')
    print('This page has:')
    for key in maintagsDict:
        if maintagsDict[key] != '0':
            temporaryTxt.append('\'' + maintagsDict[key] + ' ' + key + '\'' + '\t' + '/n')
            print('\'' + maintagsDict[key], key + '\'', '\t', end='')

def advanced(): #Function that takes an input, if it is a command execute the function of that command.
    global advYN
    while True:
        request = input('\nDo you want to see other advanced stats? (y\\n): ')
        if request == 'n' or request == 'no':
            advYN = 'no'
            return False
        elif request == 'y' or request == 'yes':
            advancedFeatureList = ['External links', 'Other tags','Tag content', 'Validate links', 'Quit']
            while True:
                print('Which stat do you want to analyze?')
                for feature in advancedFeatureList:
                    print(feature, end='\t\t')
                advRequest = input('\n Command: ')
                if advRequest not in advancedFeatureList:
                    print('Please insert a valid command.')
                elif advRequest.capitalize() == 'Quit':
                    advYN = 'no'
                    return False
                elif advRequest.capitalize() == 'External links':
                    return showExternalLink(linkDict(linkList(site)))
                elif advRequest.capitalize() == 'Other tags':
                    return showOtherTags(site)
                elif advRequest.capitalize() == 'Validate links':
                    return validateLink(linkDictValidate(linkList(site)))
                elif advRequest.capitalize() == 'Tag content':
                    return showTagContents(site)
        else:
            print('Input not valid!')

def save(): #If the user want put in the file the temporary list, if he say no, reset the temporary list and stop the while loop
    global temporaryTxt
    ans = ''
    while ans != 'y':
        ans = input('Do you want to save the output in a file? (y\\n): ')
        if ans == 'y':
            name = input('Name of the file: ')
            outputFile = open(name+'.txt', 'a')
            for i in temporaryTxt:
                outputFile.write(str(i))
        elif ans == 'n':
            temporaryTxt = []
            ans = 'y'
        else:
            print('Wrong input')

def main(): #main function that recall all the other main functions
    # global temporaryTxt
    global site
    global advYN
    site = load()
    header()
    advYN = 'yes'
    while advYN == 'yes':
        advanced()
    save()
    request = input('Do you want to quit or perform a new search? (quit/new): ')
    while request != 'quit':
        if request == 'new':
            return main()
        else:
            print('Wrong input!')
            request = input('Do you want to quit or perform a new search? (quit/new): ')
    goodbye()

main()