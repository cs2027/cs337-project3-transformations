import sys
import spacy
import re
from utils.vegetarian import MEATS, FISH, MEAT_SUBSTITUTES
from utils.healthy import UNHEALTHY_FOODS
from utils.lactose import LACTOSE_FOODS
from utils.cuisine_style import CUISINES
from recipe_loader import Recipe
from fractions import Fraction

NLP = spacy.load("en_core_web_sm")

TRANSFORMATIONS = [
  "to vegeterian", "from vegeterian", "to healthy", "to unhealthy",
  "double quantity", "half quantity", "lactose free"
]

NON_MEAT_KEYWORDS = ["broth", "soup", "sauce"]

def main(data_source, transformation):
    recipe_data = Recipe(data_source)
    valid_transformation = False
    changes = []

    if transformation == "to vegeterian":
      for ingredient in recipe_data.ingredient_quantities.keys():
        if any([keyword in ingredient for keyword in NON_MEAT_KEYWORDS]):
          continue

        if set_contains_ingredient(MEATS, ingredient):
          if "ground" in ingredient or "minced" in ingredient:
            changes.append(f"Use 'lentils' instead of {ingredient}")
          else:
            changes.append(f"Use 'tofu' instead of {ingredient}")

        if set_contains_ingredient(FISH, ingredient):
          changes.append(f"Use 'tofu' instead of {ingredient}")

      valid_transformation = True

    if transformation == "from vegeterian":
      meat_substitutes = MEAT_SUBSTITUTES.keys()

      for ingredient in recipe_data.ingredient_quantities.keys():
        if any([keyword in ingredient for keyword in NON_MEAT_KEYWORDS]):
          continue

        res = set_contains_ingredient(meat_substitutes, ingredient)

        if res:
          changes.append(f"Use '{MEAT_SUBSTITUTES[res]}' instead of {ingredient}")

      valid_transformation = True

    if transformation == "to healthy":
      unhealthy_foods = UNHEALTHY_FOODS.keys()

      for ingredient in recipe_data.ingredient_quantities.keys():
        if any([keyword in ingredient for keyword in NON_MEAT_KEYWORDS]):
          continue

        res = set_contains_ingredient(unhealthy_foods, ingredient)

        if res:
          changes.append(f"Use '{UNHEALTHY_FOODS[res]}' instead of {ingredient}")
        elif "oil" in ingredient.lower() and "olive oil" not in ingredient.lower():
          changes.append(f"Use 'olive oil' instead of {ingredient}")

      valid_transformation = True

    if transformation == "to unhealthy":
      for ingredient in recipe_data.ingredient_quantities.keys():
        if "oil" in ingredient.lower():
          changes.append(f"Use 'lard' instead of {ingredient}")
        elif "sugar" in ingredient.lower():
          changes.append(f"Use 'corn syrup' instead of {ingredient}")
        else:
          if any([keyword in ingredient for keyword in NON_MEAT_KEYWORDS]) or "bacon" in ingredient:
            continue

          if set_contains_ingredient(MEATS, ingredient) or set_contains_ingredient(FISH, ingredient):
            changes.append(f"Use 'bacon' instead of {ingredient}")

      valid_transformation = True

    if transformation == "double quantity":
      scaled_quantities = scale_ingredient_quantities(recipe_data.ingredient_quantities, 2)
      changes.append(scaled_quantities)

      valid_transformation = True

    if transformation == "half quantity":
      scaled_quantities = scale_ingredient_quantities(recipe_data.ingredient_quantities, 0.5)
      changes.append(scaled_quantities)

      valid_transformation = True

    if transformation == "lactose free":
      lactose_foods = LACTOSE_FOODS.keys()

      for ingredient in recipe_data.ingredient_quantities.keys():
        res = set_contains_ingredient(lactose_foods, ingredient)

        if res:
          changes.append(f"Use '{LACTOSE_FOODS[res]}' instead of {ingredient}")

      valid_transformation = True

    if not valid_transformation:
      [from_cuisine, to_cuisine] = transformation.split(" ")
      possible_cuisines = CUISINES.keys()

      if not from_cuisine.lower() in possible_cuisines or not to_cuisine.lower() in possible_cuisines:
        print_error_message()
        print(f"Currently only supporting cuisines: {list(possible_cuisines)}\n")
        exit(1)
      else:
        from_cuisine_data, to_cuisine_data = CUISINES[from_cuisine], CUISINES[to_cuisine]
        replacements = { "proteins": [], "spices": [], "sauces": [], "herbs": [] }

        for replacement in replacements.keys():
          for ingredient in recipe_data.ingredient_quantities.keys():
            if set_contains_ingredient(getattr(from_cuisine_data, replacement), ingredient, True):
              replacements[replacement] = replacements[replacement] + [ingredient]

          if replacements[replacement]:
            changes.append(f"Use any of '{getattr(to_cuisine_data, replacement)}' instead of {replacements[replacement]}")

        valid_transformation = True

    if valid_transformation:
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

def set_contains_ingredient(set, ingredient, inverted_loop_flag=False):
  if not inverted_loop_flag:
    subwords = ingredient.split(" ")

    for word in subwords:
      if word in set:
        return word

    return ""

  for word in set:
    if word in ingredient.lower():
      return ingredient

  return ""

def output_transformations(changes, transformation):
  if transformation in TRANSFORMATIONS:
    print(f"\n[TRANSFORMATIONS for '{transformation}']\n")
  else:
    [from_cuisine, to_cuisine] = transformation.split(" ")
    print(f"\n[TRANSFORMATIONS for '{from_cuisine}' to '{to_cuisine}']\n")

  if changes:
    if "quantity" in transformation:
      print("NEW INGREDIENT QUANTITIES:")

    for change in changes:
      print(change)
  else:
    print("No changes found")

  print()

def print_error_message():
  print()
  print("Error: Invalid transformation. Valid transformations are one of the following:\n")
  print("1. to vegeterian\n2. from vegeterian\n3. to healthy\n4. to unhealthy\n5. [from-cuisine] [to-cuisine]")
  print("6. double quantity\n7. half quantity\n8. lactose free")
  print()

if __name__ == "__main__":
    if len(sys.argv) != 4:
      print("Usage: python transformation.py [URL] [transformation string]")
      exit(1)

    main(sys.argv[1], sys.argv[2] + " " + sys.argv[3])
