import sys


def get_item(dict_, target):
    for key, item in dict_.items():
        if key.upper() == target.upper():
            return item
    return None


def get_key(dict_, target):
    for key, item in dict_.items():
        if item.upper() == target.upper():
            return key
    return None


def print_state_or_capital_city(expr):
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
    value = get_item(states, expr)
    key = get_key(capital_cities, expr)
    if value:
        print(capital_cities.get(value),
              "is the capital of",
              get_key(states, value))
    elif key:
        print(capital_cities.get(key),
              "is the capital of",
              get_key(states, key))
    else:
        print(expr, "is neither a capital city nor a state")


def main():
    if len(sys.argv) != 2:
        return
    exprs = sys.argv[1].split(",")
    for expr in exprs:
        expr = expr.strip()
        if expr == "":
            continue
        print_state_or_capital_city(expr)


if __name__ == '__main__':
    main()
