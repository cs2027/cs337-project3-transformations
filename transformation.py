import sys
import spacy
import re
from utils.vegetarian import MEATS, FISH, MEAT_SUBSTITUTES
from recipe_loader import Recipe

NLP = spacy.load("en_core_web_sm")

TRANSFORMATIONS = [
  "to vegeterian", "from vegeterian", "to south asian", "to korean",
  "double quantity", "half quantity", "lactose free"
]

def main(data_source, transformation):
    recipe_data = Recipe(data_source)

    if transformation not in TRANSFORMATIONS:
      print_error_message()
      exit(1)

    changes = []

    if transformation == "to vegeterian":
      for ingredient in recipe_data.ingredient_quantities:
        [root_ingredient, full_ingredient, _] = ingredient

        if root_ingredient.lower() in MEATS:
          if "ground" in full_ingredient or "minced" in full_ingredient:
            changes.append(f"Use 'lentils' instead of {full_ingredient}")
          else:
            changes.append(f"Use 'tofu' instead of {full_ingredient}")

        if root_ingredient.lower() in FISH:
          changes.append(f"Use 'tofu' instead of {full_ingredient}")

    if transformation == "from vegeterian":
      meat_substitutes = MEAT_SUBSTITUTES.keys()

      for ingredient in recipe_data.ingredient_quantities:
        [root_ingredient, full_ingredient, _] = ingredient

        if root_ingredient in meat_substitutes:
          changes.append(f"Use '{MEAT_SUBSTITUTES[root_ingredient]}' instead of {full_ingredient}")

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

    output_transformations(changes, transformation)

def output_transformations(changes, transformation):
  print(f"\n[TRANSFORMATIONS for '{transformation}']")

  if changes:
    for change in changes:
      print(change)
  else:
    print("No changes found")

  print()

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
    if len(sys.argv) != 4:
      print("Usage: python transformation.py [URL] [transformation string]")
      exit(1)

    main(sys.argv[1], sys.argv[2] + " " + sys.argv[3])
