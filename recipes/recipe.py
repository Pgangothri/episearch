import abc
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as url

class Recipe:
    __metaclass__ = abc.ABCMeta
    title = ''
    date = ''
    desc = ''
    ingredients = []
    directions = []
    categories = []

    @abc.abstractstaticmethod
    def get_title(self, page):
        pass

    @abc.abstractstaticmethod
    def get_ingredients(self, page):
        pass

    @abc.abstractstaticmethod
    def get_directions(self, page):
        pass

    @abc.abstractstaticmethod
    def get_categories(self, page):
        pass

    @abc.abstractstaticmethod
    def get_date(self, page):
        pass

    @abc.abstractstaticmethod
    def get_desc(self, page):
        pass

    def build_recipie(self, page):
        self.title = self.get_title(page)
        self.ingredients = self.get_ingredients(page)
        self.directions = self.get_directions(page)
        self.categories = self.get_categories(page)
        self.date = self.get_date(page)
        self.desc = self.get_desc(page)

    def __init__(self, page):
        try:
            self.build_recipie(bs(url(page), 'html.parser'))
        except Exception as x:
            print(f"Could not build recipe from {page}, {x}")

class EP_Recipe(Recipe):
    def get_title(self, page):
        return page.find('h1', {'itemprop': 'name'}).text

    def get_ingredients(self, page):
        return [i.text.strip() for i in page.find_all('li', {'itemprop': 'ingredients'})]

    def get_directions(self, page):
        return [i.text.strip() for i in page.find_all('li', {'class': 'preparation-step'})]

    def get_categories(self, page):
        return [i.text for i in page.find_all('dt', {'itemprop': 'recipeCategory'})]

    def get_date(self, page):
        try:
            return page.find('meta', {'itemprop': 'datePublished'})['content']
        except:
            return None

    def get_desc(self, page):
        try:
            return page.find('div', {'itemprop': 'description'}).find('p').text
        except:
            return None

    def build_recipie(self, page):
        super(EP_Recipe, self).build_recipie(page)
