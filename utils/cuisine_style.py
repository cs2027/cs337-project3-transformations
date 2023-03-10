class Cuisine:
  def __init__(self, proteins, spices, sauces, herbs):
    self.proteins = proteins
    self.spices = spices
    self.sauces = sauces
    self.herbs = herbs

CUISINES = {
  "korean": Cuisine(
    ["beef", "pork"],
    ["chili pepper flakes"],
    ["soybean paste", "gochujang", "soy sauce", "rice wine", "fish sauce"],
    ["kimchi", "garlic", "ginger", "scallions"]
  ),
  "mexican": Cuisine(
    ["beans", "chorizo", "chicken"],
    ["cumin", "chili powder", "cinnamon", "jalapeno", "poblano", "habanero"],
    ["salsa", "guacamole", "mole"],
    ["cilantro", "basil", "rosemary", "thyme", "sage", "lime"]
  )
}
