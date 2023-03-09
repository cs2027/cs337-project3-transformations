import sys
import spacy
import re
from pyyoutube import Api
from googlesearch import search
from recipe_loader import Recipe

NLP = spacy.load("en_core_web_sm")
API = Api(api_key="AIzaSyCFOl8vv1md_YmVgkmYvQ9O_MZCgmkCYlc")

TRANSFORMATIONS = [
  "to vegeterian", "from vegeterian", "to south asian", "to korean",
  "double quantity", "half quantity", "lactose free"
]

def main(data_source, transformation):
    print("Loading, parsing recipe data")
    recipe_data = Recipe(data_source)
    print("Done loading recipe data!\n")

    print(recipe_data.ingredients)
    print(recipe_data.ingredient_quantities)

    if transformation not in TRANSFORMATIONS:
      print_error_message()
      exit(1)

    if transformation == "to vegeterian":
      pass

    if transformation == "from vegeterian":
      pass

    if transformation == "to south asian":
      pass

    if transformation == "to korean":
      pass

    if transformation == "double quantity":
      pass

    if transformation == "half quantity":
      pass

    if transformation == "lactose free":
      pass


def ingredient_lookup(quantities, query):
  for ingredient, quantity in quantities.items():
    if query in ingredient:
      return quantity

  return None

def print_error_message():
  print()
  print("Error: Invalid transformation. Valid transformations are one of the following:")
  print("1. to vegeterian\n2. from vegeterian\n3.to south asian\n4. to korean")
  print("5. double quantity\n6.half quantity\n7.lactose free")
  print()

if __name__ == "__main__":
    if len(sys.argv) != 3:
      print("Usage: python transformation.py [URL] [transformation]")
      exit(1)

    main(sys.argv[1], sys.argv[2])
