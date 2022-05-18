def read_target():
    with open("numbers.txt", 'r') as f:
        for line in f.readlines():
            print(*line.strip().split(","), sep="\n")


if __name__ == '__main__':
    read_target()

