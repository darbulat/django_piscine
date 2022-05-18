from local_lib.path import Path


def main():
    Path('folder').mkdir_p()
    f = Path('folder/file.txt')
    f.write_text("Hello world!")
    print(f.read_text())


if __name__ == '__main__':
    main()
