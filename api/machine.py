from threading import Lock

from .ingredient import Ingredient
from .beverage import Beverage

mutex = Lock()

class BrewingMachine:
    """
    Brewing Machine consists of some outlets and storage compartments to store ingredients(raw materials)
    """
    def __init__(self, outlets=1, ingredient_to_store={}, beverage_configs={}):

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
        for item_name, item_quantity in ingredients.items():
            ingredient_instance = self.ingredient_store.get(item_name)
            if ingredient_instance:
                ingredient_instance.refill(item_quantity)

    def create_beverages_offered_by_machine(self, beverage_configs):
        for beverage_name, config in beverage_configs.items():
            beverage_instance = Beverage(beverage_name, ingredient_config=config)
            self.beverages_offered_by_machine[beverage_name] = beverage_instance 

    def _check_is_beverage_exists(self, name):
        return True if self.beverages_offered_by_machine.get(name) else False

    def _check_if_beverage_can_be_prepared(self, beverage_name):
        if self._check_is_beverage_exists(beverage_name) is False:
            return False
        beverage = self.beverages_offered_by_machine[beverage_name]
        for name, req_ingredient_instance in beverage.required_ingredients_config.items():
            ingredient_in_store = self.ingredient_store.get(name, None)
            if ingredient_in_store:
                if ingredient_in_store < req_ingredient_instance:
                    print("{beverage} can not be prepared because because ingredient {name} is not sufficient".format(
                            beverage=beverage_name, name=req_ingredient_instance.name
                        ))
                    return False
            else:
                print("{beverage} can not be prepared because ingredient {name} is not available".format(
                        beverage=beverage_name, name=name 
                    ))
                return False
        return True

    def prepare_beverage(self, beverage_name):
        mutex.acquire()
        # print("Preparing Beverage", beverage_name)
        try:
            if self._check_if_beverage_can_be_prepared(beverage_name):
                beverage = self.beverages_offered_by_machine[beverage_name]
                for name, req_ingredient in beverage.required_ingredients_config.items():
                    ingredient_in_store = self.ingredient_store.get(name)
                    ingredient_in_store.quantity_in_ml -= req_ingredient.quantity_in_ml
                print("{} is prepared".format(beverage_name))
                return beverage
            return None
        except Exception as e:
            print("Exception***",e)
        finally:
            mutex.release()

