from sqlalchemy.util import counter


class card:
    def __init__(self, name, id, card_type, color, cost, life, effect, type, counter, power, attribute, block, collection_name, collection_id, trigger, trigger_effect):
        self.id = id
        self.name = name
        self.card_type = card_type
        self.color = color
        self.cost = cost
        self.life = life
        self.effect = effect
        self.type = type
        self.counter = counter
        self.power = power
        self.attribute = attribute
        self.block = block
        self.collection_name = collection_name
        self.collection_id = collection_id,
        self.trigger = trigger
        self.trigger_effect = trigger_effect



    def __str__(self):
        return f"Card(Name: {self.name}, ID: {self.id}, Type: {self.card_type}, Color: {self.color}, Cost: {self.cost}, Life: {self.life}, Effect: {self.effect}, Type: {self.type}, Counter: {self.counter}, Power: {self.power}, Attribute: {self.attribute}, Block: {self.block}, Collection Name: {self.collection_name}, Collection ID: {self.collection_id}, Trigger: {self.trigger}, Trigger Effect: {self.trigger_effect})"