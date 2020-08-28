import os
import json
import argparse
import random
from threading import Thread

# low level APIs to interact with brewing machine
from api.machine import BrewingMachine, parse_and_create_brewing_machine_from_json

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
    brewing_machine = parse_and_create_brewing_machine_from_json(parsed_json)
    # print(brewing_machine)
    all_offered_beverages = list(brewing_machine.beverages_offered_by_machine.keys())

    for outlet in range(brewing_machine.outlets):
        # pick any random beverage offered by our brewing machine
        beverage_name = random.choice(all_offered_beverages)
        t = Thread(target=brewing_machine.prepare_beverage, args=(beverage_name,))
        t.start()



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)

# NOTE:
# Python2 vs Python3 
###########################################
# Case of print function and thread safety 
############################################
# If you run this with python2 i.e. `python2 app.py` , it might show one/two  extra newlines 
# because print function in python2.7 is not thread safe
# however if you run it with python3 like `python3 app.py`, print function will work perfectly fine 