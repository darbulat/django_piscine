#!/usr/bin/python3
import os
import sys
import settings


def main():
    if len(sys.argv) != 2:
        return print("Wrong number of argument")
    path = sys.argv[1]
    if not path.endswith(".template"):
        return print("Wrong extension, required *.template")
    if not os.path.isfile(path):
        return print(f"File does not exit: {path}")
    with open(path, "r") as f:
        template = "".join(f.readlines())
    file = template.format(**vars(globals()['settings']))
    path = path.replace(".template", ".html")
    with open(path, "w") as f:
        f.write(file)


if __name__ == '__main__':
    main()
