import sys

from huffman import huffman, stringify

def main():
    args = sys.argv

    if len(args) != 2:
        print("nope")

        return

    codes = huffman(args[1])

    for code in codes.items():
        print("'%s' -> %s" % code)

    print(stringify(args[1], codes))

if __name__ == "__main__":
    main()
