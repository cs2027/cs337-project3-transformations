import sys
import spacy
import re
from utils.vegetarian import MEATS, FISH, MEAT_SUBSTITUTES
from utils.healthy import UNHEALTHY_FOODS
from recipe_loader import Recipe
from fractions import Fraction

NLP = spacy.load("en_core_web_sm")

TRANSFORMATIONS = [
  "to vegeterian", "from vegeterian", "to healthy", "to unhealthy",
  "to south asian", "to korean", "double quantity", "half quantity", "lactose free"
]

def main(data_source, transformation):
    recipe_data = Recipe(data_source)

    if transformation not in TRANSFORMATIONS:
      print_error_message()
      exit(1)

    changes = []

    if transformation == "to vegeterian":
      for ingredient in recipe_data.ingredient_quantities.keys():
        if set_contains_ingredient(MEATS, ingredient):
          if "ground" in ingredient or "minced" in ingredient:
            changes.append(f"Use 'lentils' instead of {ingredient}")
          else:
            changes.append(f"Use 'tofu' instead of {ingredient}")

        if set_contains_ingredient(FISH, ingredient):
          changes.append(f"Use 'tofu' instead of {ingredient}")

    if transformation == "from vegeterian":
      meat_substitutes = MEAT_SUBSTITUTES.keys()

      for ingredient in recipe_data.ingredient_quantities.keys():
        res = set_contains_ingredient(meat_substitutes, ingredient)

        if res:
          changes.append(f"Use '{MEAT_SUBSTITUTES[res]}' instead of {ingredient}")

    if transformation == "to healthy":
      unhealthy_foods = UNHEALTHY_FOODS.keys()

      for ingredient in recipe_data.ingredient_quantities.keys():
        res = set_contains_ingredient(unhealthy_foods, ingredient)

        if res:
          changes.append(f"Use '{UNHEALTHY_FOODS[res]}' instead of {ingredient}")
        elif "oil" in ingredient.lower() and "olive oil" not in ingredient.lower():
          changes.append(f"Use 'olive oil' instead of {ingredient}")

    if transformation == "to unhealthy":
      for ingredient in recipe_data.ingredient_quantities.keys():

        if "oil" in ingredient.lower():
          changes.append(f"Use 'lard' instead of {ingredient}")
        elif "sugar" in ingredient.lower():
          changes.append(f"Use 'corn syrup' instead of {ingredient}")
        else:
          if "bacon" in ingredient:
            continue

          if set_contains_ingredient(MEATS, ingredient) or set_contains_ingredient(FISH, ingredient):
            changes.append(f"Use 'bacon' instead of {ingredient}")

    if transformation == "to south-asian":
      pass

    if transformation == "to east-asian":
      pass

    if transformation == "double quantity":
      scaled_quantities = scale_ingredient_quantities(recipe_data.ingredient_quantities, 2)
      changes.append(scaled_quantities)

    if transformation == "half quantity":
      scaled_quantities = scale_ingredient_quantities(recipe_data.ingredient_quantities, 0.5)
      changes.append(scaled_quantities)

    if transformation == "lactose free":
      pass

    output_transformations(changes, transformation)

def scale_ingredient_quantities(quantities, factor):
  res = {k : "" for k in quantities.keys()}

  for ingredient, quantity in quantities.items():
    [amount, unit, _] = quantity

    if amount == -1:
      continue

    if amount.isnumeric():
      amount = float(amount)
    else:
      amount = float(Fraction(amount))

    amount *= factor

    res[ingredient] = f"{amount} {unit}" if unit else f"{amount}"

  return res

def set_contains_ingredient(set, ingredient):
  subwords = ingredient.split(" ")

  for word in subwords:
    if word in set:
      return word

  return ""

def output_transformations(changes, transformation):
  print(f"\n[TRANSFORMATIONS for '{transformation}']\n")

  if changes:
    if "quantity" in transformation:
      print("NEW INGREDIENT QUANTITIES:")
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
  print("Error: Invalid transformation. Valid transformations are one of the following:\n")
  print("1. to vegeterian\n2. from vegeterian\n3. to healthy\n4. to unhealthy\n5. to south-asian")
  print("6. to east-asian\n7. double quantity\n8. half quantity\n9. lactose free")
  print()

if __name__ == "__main__":
    if len(sys.argv) != 4:
      print("Usage: python transformation.py [URL] [transformation string]")
      exit(1)

    main(sys.argv[1], sys.argv[2] + " " + sys.argv[3])
