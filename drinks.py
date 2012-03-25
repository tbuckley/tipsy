import pickle, glob
import re
import persistance

# def lev_distance(a, b, custom_costs=None):
#     costs = {
#         'insert': 1,
#         'delete': 1,
#         'replace': 1,
#         'match': 0,
#         'base': 0
#     }
#     costs.update(custom_costs or {})
#     dists = {}
#     def helper(a, b):
#         if (len(a), len(b)) in dists:
#             return dists[(len(a), len(b))]
#         if len(a) == 0:
#             val = costs['base'] + (costs['insert'] * len(b))
#         elif len(b) == 0:
#             val = costs['base'] + (costs['delete'] * len(a))
#         else:
#             match_replace = costs['match'] if a[0] == b[0] else costs['replace']
#             val = min(
#                 costs['insert'] + helper(a, b[1:]), # insert
#                 costs['delete'] + helper(a[1:], b), # delete
#                 match_replace + helper(a[1:], b[1:]) # replace/match
#             )
#         dists[(len(a), len(b))] = val
#         return val
#     return helper(a, b)

class DrinkDatabase(object):
    def __init__(self, recipes, ingredients):
        """Creates a class given the recipes and ingredients
        
        recipes - an array of recipes, each of which consists of:
          - [string] url
          - [string] title
          - [array] ingredients = array of {id: int, amount: string}
          - [tuple] rating = () if none, (value, # votes) otherwise
         
        ingredients - array
          - list of ingredient names (map from id -> name)
        """
        self.recipes = dict(enumerate(recipes))
        self.ingredients = dict(enumerate(ingredients))
    
    def create_ingredient_map(self):
        self.ingredient_map = {}
        for i in enumerate(self.recipes):
            recipe = self.recipes[i]
            for ingr in recipe['ingredients']:
                ingr_id = ingr['id']
                if ingr_id not in self.ingredient_map:
                    self.ingredient_map[ingr_id] = set()
                self.ingredient_map[ingr_id].add(recipe)
    
    def find_matching_ingredients(self, search):
        search = search.lower()
        ingrs = []
        for i in self.ingredients:
            name = self.ingredients[i].lower()
            m = re.match("(.*%s.*)" % search, name)
            if m:
                ingrs.append(i)
        return ingrsm

def find_matching_ingredients(search, ingredients):
    ingrs = []
    for i, name in enumerate(ingredients['list']):
        if lev_distance(search.lower(), name.lower(), {'insert': 0}) == 0:
            ingrs.append(i)
        #m = re.match("(.*%s.*)" % search.lower(), name.lower())
        #if m:
        #    ingrs.append(i)
    return ingrs

def ingredient_names(ingredients, *ids):
    return [ingredients['list'][i] for i in ids]

def main():
    print "Loading data..."
    recipes, ingredients = persistance.load_latest_snapshot()
    
    print "Generating ingredient map..."
    ingredient_map = make_ingredient_map(recipes, ingredients)
    print "Initialized: %d recipes, %d ingredients" % (len(recipes), len(ingredients['list']))
    while True:
        ingr = raw_input("Ingredient: ")
        ingrs = find_matching_ingredients(ingr, ingredients)
        
        print "Matches: %d" % len(ingrs)
        print ", ".join(ingredient_names(ingredients, *ingrs))
        
        for i in ingrs:
            print ingredients['list'][i]
            # if i in ingredient_map:
            #     for r in ingredient_map[i]:
            #         print "  " + recipes[r]['title']
        print "\n"
if __name__ == '__main__':
    main()