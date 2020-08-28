import os
import json
import argparse
import random
from threading import Thread

# low level APIs to interact with brewing machine
from api.machine import BrewingMachine

# Parser for CLI
parser = argparse.ArgumentParser(description="Brewing Machine CLI")
parser.add_argument("--json", help="Input JSON file to create brewing machine", type=lambda x: is_valid_json(parser, x), required=True)

def is_valid_json(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        try:
            f = open(arg, 'r')
            return json.load(f)
        except Exception as e:
            print(e)
            parser.error("JSON parsing error")

# main driver application
def main(args):
    parsed_json = args.json
    outlets = parsed_json["machine"]["outlets"]["count_n"]
    ingredients_to_store = parsed_json["machine"]["total_items_quantity"]
    beverage_configs = parsed_json["machine"]["beverages"]
    brewing_machine = BrewingMachine(outlets=outlets,
        ingredient_to_store=ingredients_to_store, beverage_configs=beverage_configs
    )
    # print(brewing_machine)
    all_offered_beverages = list(brewing_machine.beverages_offered_by_machine.keys())

    for outlet in range(outlets):
        # print("Outlet-", outlet+1)
        beverage_name = random.choice(all_offered_beverages)
        # print(beverage_name)
        p = Thread(target=brewing_machine.prepare_beverage, args=(beverage_name,))
        p.start()



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
