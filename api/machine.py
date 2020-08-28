from threading import Lock

from .ingredient import Ingredient
from .beverage import Beverage

mutex = Lock()

class BrewingMachine:
    """
    Brewing Machine consists of some outlets and storage compartments to store ingredients(raw materials)
    """
    def __init__(self, outlets=1, ingredient_to_store={}, beverage_configs={}):
        self.__logger__ = ""
        self.outlets = outlets
        
        #key-val => ingredient_name: ingredient_instance
        self.ingredient_store = {}
        
        # key-val => beverage_name: beverage_instance
        self.beverages_offered_by_machine = {}

        # initialize ingredients stored in our machine
        self.create_ingredient_store(ingredient_to_store)

        self.create_beverages_offered_by_machine(beverage_configs)

    def __str__(self):
        return "N={}\n\ningredients={}\n\nbeverages={}".format(self.outlets, self.ingredient_store, self.beverages_offered_by_machine)

    def create_ingredient_store(self, ingredients={}):
        for item_name, item_quantity in ingredients.items():
            ingredient_instance = Ingredient(item_name, item_quantity)
            self.ingredient_store[item_name] = ingredient_instance
    
    def refill_ingredients(self, ingredients = {}):
        for item_name, ingredient_config in ingredients.items():
            ingredient_instance = self.ingredient_store.get(item_name)
            if ingredient_instance:
                ingredient_instance.refill_from_ingredient_config(ingredient_config)

    def create_beverages_offered_by_machine(self, beverage_configs):
        for beverage_name, config in beverage_configs.items():
            beverage_instance = Beverage(beverage_name, ingredient_config=config)
            self.beverages_offered_by_machine[beverage_name] = beverage_instance 

    def _check_is_beverage_exists(self, name):
        return True if self.beverages_offered_by_machine.get(name) else False

    def _check_if_beverage_can_be_prepared(self, beverage_name):
        # check if beverage is offered by machine or not
        if self._check_is_beverage_exists(beverage_name) is False:
            return False
        beverage = self.beverages_offered_by_machine[beverage_name]
        # sorted alphabetically by ingredient name, so that tests can be done properly
        for name, req_ingredient_instance in sorted(beverage.required_ingredients_config.items()):
            ingredient_in_store = self.ingredient_store.get(name, None)
            # check if ingredient is stored in brewing machine or not
            if ingredient_in_store:
                # check if ingredient is sufficeint or not
                if ingredient_in_store < req_ingredient_instance:
                    self.__logger__ = "{beverage} can not be prepared because ingredient {name} is not sufficient".format(
                            beverage=beverage_name, name=req_ingredient_instance.name
                        )
                    return False
            else:
                self.__logger__ = "{beverage} can not be prepared because ingredient {name} is not available".format(
                        beverage=beverage_name, name=name 
                    )
                return False
        return True

    def prepare_beverage(self, beverage_name):
        mutex.acquire()
        try:
            # check if we have enough(required) ingredients to prepare beverage
            if self._check_if_beverage_can_be_prepared(beverage_name):
                beverage = self.beverages_offered_by_machine[beverage_name]
                # sorted alphabetically by ingredient name, so that automated testing can be done properly
                for name, req_ingredient in sorted(beverage.required_ingredients_config.items()):
                    ingredient_in_store = self.ingredient_store.get(name)
                    # use ingredients as per requiremnts
                    ingredient_in_store.quantity_in_ml -= req_ingredient.quantity_in_ml
                self.__logger__ = "{} is prepared".format(beverage_name)
                print(self.__logger__)
                return beverage
            print(self.__logger__)
            return None
        except Exception as e:
            print("Exception***",e)
        finally:
            mutex.release()



def parse_and_create_brewing_machine_from_json(data):
    outlets = data["machine"]["outlets"]["count_n"]
    ingredients_to_store = data["machine"]["total_items_quantity"]
    beverage_configs = data["machine"]["beverages"]
    brewing_machine = BrewingMachine(outlets=outlets,
        ingredient_to_store=ingredients_to_store, beverage_configs=beverage_configs
    )
    return brewing_machine