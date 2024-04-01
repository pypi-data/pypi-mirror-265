"""Web's base file"""
import bs4
import requests


def getStrFromUrl(url: str):
    return requests.get(url).text


def getBSFromUrl(url: str, parser: str = 'html.parser'):
    pageStr = getStrFromUrl(url)
    return bs4.BeautifulSoup(pageStr, features=parser)


def getBSFromText(pageStr: str, parser: str = 'html.parser'):
    return bs4.BeautifulSoup(pageStr, features=parser)


def getBSFromFile(filePath: str, parser: str = 'html.parser'):
    pageStr = ''
    with open(filePath, 'r') as f:
        pageStr += f.read()
    return bs4.BeautifulSoup(pageStr, features=parser)
