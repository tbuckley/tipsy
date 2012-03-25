import pickle, glob

def paths_for_tag(tag='all'):
    if type(tag) is int:
        tag = '%05d' % tag
    base_recipes = 'data/recipes_%s.pickle'
    base_ingredients = 'data/ingredients_%s.pickle'
    return (base_recipes % tag, base_ingredients % tag)

def load_pickle(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data

def save_pickle(data, path):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def largest_tag():
    # try:
    tags = [s[13:-7] for s in glob.glob("data/recipes_*")]
    if 'all' in tags:
        return 'all'
    return max([int(t) for t in tags])
    # except Exception:
        # return None
    
def save_snapshot(recipes, ingredients, tag='all'):
    recipe_path, ingredient_path = paths_for_tag(tag)
    save_pickle(recipes, recipe_path)
    save_pickle(ingredients, ingredient_path)
    
def load_snapshot(tag='all'):
    """Load the specified snapshot from pickled files"""
    recipe_path, ingredient_path = paths_for_tag(tag)
    return (load_pickle(recipe_path), load_pickle(ingredient_path))

def default_stores():
    """Return default values for recipes and ingredients"""
    recipes = []
    ingredients = {
        'list': [],
        'lookup': {}
    }
    return recipes, ingredients

def load_latest_snapshot():
    tag = largest_tag()
    print tag
    if tag:
        return load_snapshot(tag)
    return default_stores()

def load_latest_ctr():
    tag = largest_tag()
    return (tag if type(tag) is int else 1000000000)