import sys


def print_capital_city(key: str):
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }
    print(capital_cities[states[key]])


def main():
    if len(sys.argv) == 2:
        try:
            print_capital_city(sys.argv[1])
        except KeyError:
            print("Unknown state")


if __name__ == '__main__':
    main()
