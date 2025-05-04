import random

def generate_random_baggage():
    items = ["Book", "Laptop", "Knife", "Telephone", "Tablet", "Camera"]
    weights = [18, 18, 10, 18, 18, 18]
    return random.choices(items, weights=weights, k=random.randint(5, 10))