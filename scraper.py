import urllib2
from BeautifulSoup import BeautifulSoup
import re
import persistance

def fetch_page(url):
    page = urllib2.urlopen(url)
    try:
        return BeautifulSoup(page, convertEntities=BeautifulSoup.HTML_ENTITIES)
    except TypeError:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        return BeautifulSoup(str(soup), convertEntities=BeautifulSoup.HTML_ENTITIES)

def fetch_recipes(page=1):
    listing_url = "http://www.drinksmixer.com/cat/1/%d/"
    recipe_url = "http://www.drinksmixer.com"
    i = page # @TODO: set to 1
    while True:
        soup = fetch_page(listing_url % i)
        content = soup.find("div", {"class": "clr"})
        # Check to make sure there are recipes
        if content.text == u'No recipes listed.':
            break
        recipes = [(recipe_url+r['href'], r.text) for r in content.findAll('a')]
        for r in recipes:
            yield r
        i += 1 # move to next page

def register_ingredient(ingr, ingredients):
    if ingr not in ingredients['lookup']:
        ingredients['list'].append(ingr)
        ingredients['lookup'][ingr] = len(ingredients['list'])
    return ingredients['lookup'][ingr]

title_re = re.compile("recipe_title")
ingredient_re = re.compile("ingredient")
instructions_re = re.compile("instructions")
rating_re = re.compile("rating")
def fetch_recipe(url, ingredients_data):
    soup = fetch_page(url)
    title = soup.find("h1", {"class": title_re}).text
    ingredients = soup.findAll("span", {"class": ingredient_re})
    instructions = soup.find("div", {"class": instructions_re}).text
    ingrs = []
    for i in ingredients:
        amount = i.find(attrs={"class":"amount"}).text
        name = i.find(attrs={"class":"name"}).text
        ingr_id = register_ingredient(name, ingredients_data)
        ingrs.append({'id': ingr_id, 'amount': amount})
    instructions = soup.find("div", {"class": instructions_re}).text
    rating_info = soup.find("div", {"class": rating_re}).div
    rating_tuple = ()
    if len(rating_info) > 3:
        rating = float(rating_info.div.text)
        votes = int(rating_info.find("span", {"class": "count"}).text)
        rating_tuple = (rating, votes)
    return {
        "url": url,
        "title": title,
        "ingredients": ingrs,
        "instructions": instructions,
        "rating": rating_tuple
    }

def main():
    recipes, ingredients = persistance.load_latest_snapshot()
    ctr = persistance.load_latest_ctr()
    
    print "Initialized: %d recipes, %d ingredients" % (len(recipes), len(ingredients['list']))
    
    for recipe_url, name in fetch_recipes((ctr / 100) + 1):
        print "Reading %s" % name, recipe_url
        recipes.append(fetch_recipe(recipe_url, ingredients))
        ctr += 1
        if ctr % 100 == 0:
            save_snapshot(recipes, ingredients, ctr)
    
    persistance.save_snapshot(recipes, ingredients)

if __name__ == '__main__':
    main()