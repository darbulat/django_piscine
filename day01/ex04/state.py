import sys


def dict_get_key_from_value(dict_, value):
    for key, item in dict_.items():
        if item == value:
            return key
    return None


def print_state(value):
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

    value = dict_get_key_from_value(capital_cities, value)
    if not value:
        print("Unknown capital city")
    else:
        print(dict_get_key_from_value(states, value))


def main():
    if len(sys.argv) == 2:
        print_state(sys.argv[1])


if __name__ == '__main__':
    main()
