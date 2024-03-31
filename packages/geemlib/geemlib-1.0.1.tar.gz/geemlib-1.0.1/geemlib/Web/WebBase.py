"""Web's base file"""
import bs4
import requests


def getStrFromUrl(url: str):
    return requests.get(url).text


def getBSFromUrl(url: str, parser: str = 'html.parser'):
    pageStr = getStrFromUrl(url)
    return bs4.BeautifulSoup(pageStr, features=parser)
