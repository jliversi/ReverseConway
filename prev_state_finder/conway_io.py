from json import dump, load, JSONDecodeError
from util import print_now

def save_results(results, depth):
    print(f'{print_now()} - Storing depth-{depth} solution in json/output/{depth}.json...')
    with open(f'json/output/{depth}.json','w+') as json_f:
        dump(results,json_f)

def load_input():
    with open('json/input.json') as f:
        try:
            result = load(f)
        except JSONDecodeError:
            print("Error loading json pattern in json/input.json.")
            quit()
    
    # check initial grid is a rectangle
    if not isinstance(result, list):
        print("Error loading json pattern in json/input.json (make sure file is a json array, not a json object)")
        quit()
    if not isinstance(result[0], list):
        print("Error loading json pattern in json/input.json (make sure file is a 2D json array)")
        quit()
    
    lens = list(map(lambda x: len(x), result))
    is_rect = all(element == lens[0] for element in lens)
    if not is_rect:
        print("Error loading json pattern in json/input.json (make sure file is a rectangle array)")
        quit()
    return result
    