import inputed
import fd
import dir


def main():
    pair = inputed.starter()
    try:
        if pair[0]:
            fd.spec(pair[1])
        else:
            dir.spec(pair[1])
    except TypeError:
        print(end="")


if __name__ == '__main__':
    main()
