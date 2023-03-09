# Will use tofu for non-ground meat, lentils for ground meat
MEATS = set([
  "pork", "chicken", "beef", "goat", "sheep", "mutton", "lamb",
  "turkey", "duck", "buffalo", "bison", "rabbit", "venison",
  "bacon", "sausage", "spam", "ham"
])

# Will use tofu as substitutes for all fish
FISH = set([
  "tuna", "salmon", "cod", "tilapia", "sardines", "catfish",
  "carp", "anchovies", "kingfish", "pollock", "trout",
  "bass", "halibut", "eel"
])

MEAT_SUBSTITUTES = {
  "tofu": "chicken", "tempeh": "chicken", "lentils": "ground beef",
  "seitan": "chicken", "jackfruit": "pork", "chickpeas": "ground beef"
}
