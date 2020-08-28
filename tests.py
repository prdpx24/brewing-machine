import unittest
from api.machine import BrewingMachine, parse_and_create_brewing_machine_from_json

config = {
            "machine": {
                "outlets": {
                    "count_n": 3
                },
                "total_items_quantity": {
                    "hot_water": 500,
                    "hot_milk": 50,
                    "ginger_syrup": 100,
                    "sugar_syrup": 60,
                    "tea_leaves_syrup": 100
                },
                "beverages": {
                    "hot_tea": {
                        "hot_water": 200,
                        "hot_milk": 100,
                        "ginger_syrup": 10,
                        "sugar_syrup": 10,
                        "tea_leaves_syrup": 30
                    },
                    "hot_coffee": {
                        "hot_water": 100,
                        "ginger_syrup": 30,
                        "hot_milk": 400,
                        "sugar_syrup": 50,
                        "tea_leaves_syrup": 30
                    },
                    "green_tea": {
                        "hot_water": 100,
                        "ginger_syrup": 30,
                        "sugar_syrup": 50,
                        "green_mixture": 30
                    },
                    "hot_flavored_milk": {
                        "hot_milk": 500,
                        "sugar_syrup": 100
                    }
                }
            }
    }
class TestBrewingMachine(unittest.TestCase):
    
    def test_prepare_hot_tea(self):
        brewing_machine = parse_and_create_brewing_machine_from_json(config)
        brewing_machine.prepare_beverage("hot_tea")
        self.assertEqual(brewing_machine.__logger__, "hot_tea can not be prepared because ingredient hot_milk is not sufficient")
        
        # refill with hot_milk
        print("refilling with hot_milk:",200)
        brewing_machine.refill_ingredients(ingredients={"hot_milk":{"hot_milk":200}})
        brewing_machine.prepare_beverage("hot_tea")
        self.assertEqual(brewing_machine.__logger__, "hot_tea is prepared")
        # prepare again
        brewing_machine.prepare_beverage("hot_tea")
        self.assertEqual(brewing_machine.__logger__, "hot_tea is prepared")
        brewing_machine.prepare_beverage("hot_tea")
        self.assertEqual(brewing_machine.__logger__, "hot_tea can not be prepared because ingredient hot_milk is not sufficient")


    def test_prepare_green_tea(self):
        brewing_machine = parse_and_create_brewing_machine_from_json(config)
        brewing_machine.prepare_beverage("green_tea")
        self.assertIn("green_tea can not be prepared", brewing_machine.__logger__)
        # no refill, because we have not created sepearet storage for green_mixture in brewing machine
        # refill can be done only on available storage(i.e. compartments in brewing machine)
    
    def test_prepare_hot_coffee(self):
        brewing_machine = parse_and_create_brewing_machine_from_json(config)
        brewing_machine.prepare_beverage("hot_coffee")
        self.assertEqual(brewing_machine.__logger__, "hot_coffee can not be prepared because ingredient hot_milk is not sufficient")
        print("refilling with hot_milk:",1000)
        brewing_machine.refill_ingredients(ingredients={"hot_milk":{"hot_milk":1000}})
        brewing_machine.prepare_beverage("hot_coffee")
        self.assertEqual(brewing_machine.__logger__, "hot_coffee is prepared")
        brewing_machine.prepare_beverage("hot_coffee")
        self.assertEqual(brewing_machine.__logger__, "hot_coffee can not be prepared because ingredient sugar_syrup is not sufficient")

    def test_prepare_hot_flavored_milk(self):
        brewing_machine = parse_and_create_brewing_machine_from_json(config)
        brewing_machine.prepare_beverage("hot_flavored_milk")
        self.assertEqual(brewing_machine.__logger__, "hot_flavored_milk can not be prepared because ingredient hot_milk is not sufficient")
        print("refilling with hot_milk:",1000)
        brewing_machine.refill_ingredients(ingredients={"hot_milk":{"hot_milk":1000}})
        brewing_machine.prepare_beverage("hot_flavored_milk")
        self.assertEqual(brewing_machine.__logger__ ,"hot_flavored_milk can not be prepared because ingredient sugar_syrup is not sufficient")



if __name__ == "__main__":
    unittest.main()

