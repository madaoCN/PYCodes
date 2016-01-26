# coding=utf8
import  urllib
from  bs4 import BeautifulSoup
import re, datetime, random

page = set()
random.seed(datetime.datetime.now())

# retrieves a list of all internal link found on a page
def getInternalLinks(bsObj, includeUrl):
    interalLinks = []
    # find all links that begin with a "/"
    for link in bsObj.findAll("a",  href=re.compile("^(/|.*"+includeUrl+")"))
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in interalLinks
                interalLinks.append(link.attrs['href'])
    return  interalLinks

# retrieves a list of all external link found on a page
def getExternalLinks(baseObj, excludeUrl):
    externalLinks = []
    # Find all link that start with http or www  that do not coantain the current URL
    for link in baseObj.findAll('a', href=re.compile("^(http|www)((?!" + excludeUrl+ ").)*$"))
        if link is not None:
            if link not  in externalLinks:
                excludeUrl.append(link.attrs["href"])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", " ").splite("/")
    return addressParts

def getRandomExternalLinks(stratingPage):
    html = urlopen(staringPage)
    basObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0
        internalLinks = getInternalLinks(stratingPage)
        return getInternalLinks(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(internalLinks]

def followExternalOnly(startSite)
        externalLink = getRandomExternalLinks("http://oreilly.com")
        print externalLink
        followExternalOnly(externalLink)