from .ingredient import Ingredient


class Beverage:
    def __init__(self, name, ingredient_config={}):
        self.name = name

        # key:val => ingredient_name : ingredient_instance
        self.required_ingredients_config = {}

        self.create_config_to_prepare_one_beverage(ingredient_config=ingredient_config)

    def create_config_to_prepare_one_beverage(self, ingredient_config={}):
        for item_name, item_quantity in ingredient_config.items():
            ingredient = Ingredient(item_name, quantity_in_ml=item_quantity)
            self.required_ingredients_config[ingredient.name] = ingredient

    def __str__(self):
        return "{} - contains {}".format(self.name, self.required_ingredients_config)

    def __repr__(self):
        return self.__str__()