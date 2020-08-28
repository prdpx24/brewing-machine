class Ingredient:
    def __init__(self, name, quantity_in_ml):
        self.name = name
        self.quantity_in_ml = quantity_in_ml

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "{} - {}".format(self.name, self.quantity_in_ml)
    
    def refill_from_ingredient_config(self, ingredient_config):
        quantity_in_ml = ingredient_config.get(self.name)
        self.refill(quantity_in_ml)

    def refill(self, quantity_in_ml):
        if self.quantity_in_ml > 0:
            self.quantity_in_ml = self.quantity_in_ml + quantity_in_ml
        else:
            self.quantity_in_ml = quantity_in_ml

    def is_empty(self):
        if self.quantity_in_ml is None or self.quantity_in_ml == 0:
            return True
        return False

    def __gt__(self, other):
        return True if self.quantity_in_ml > other.quantity_in_ml else False

    def __lt__(self, other):
        return True if self.quantity_in_ml < other.quantity_in_ml else False

    def __eq__(self, other):
        return True if self.quantity_in_ml == other.quantity_in_ml else False
