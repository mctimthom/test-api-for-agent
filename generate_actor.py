import requests
import sys
import random

API_URL = 'http://127.0.0.1:5000/create_actor'

FIRST_NAMES = [
    "Bubba",
    "Trixie",
    "Wobblebottom",
    "Fergus",
    "Chiquita",
    "Binky",
    "Flapjack",
    "Murgatroyd",
    "Periwinkle",
    "Cletus"
]

LAST_NAMES = [
    "McSnortle",
    "Wobbleworth",
    "Noodleman",
    "Quackenbush",
    "Gigglesworth",
    "Blunderpants",
    "Bumblebee",
    "Whifflebottom",
    "Fiddlesticks",
    "Dingleberry"
]


def generate_actor_data():
    return {
        "first_name": random.choice(FIRST_NAMES),
        "last_name": random.choice(LAST_NAMES)
    }



if __name__ == '__main__':
    print(len(sys.argv))
    if len(sys.argv) <= 1:
        count = 1
    else:
        count = sys.argv[1]

    for _ in range(count):
        actor_data = generate_actor_data()
        response = requests.post(API_URL, json=actor_data)
        if response.status_code == 201:
            print("created actor")
            print(response.json())
        else:
            print(response.status_code)
            print("failed to create actor")
            print(response.text)
            break
