"""
Provides top-level functions for encoding and decoding with Huffman coding.
"""

class HuffmanNode():
    """
    Node of a Huffman Tree.
    """

    def __init__(self, symbol, weight):
        self.symbol = symbol
        self.weight = weight
        self.left = None
        self.right = None

    def table(self, code=""):
        """
        Returns a dict with all symbols and their respective codes.
        """

        code_table = {}

        if self.symbol:
            code_table[self.symbol] = code if code else "0"

        if self.left:
            code_table.update(self.left.table(code + "0"))

        if self.right:
            code_table.update(self.right.table(code + "1"))

        return code_table

class HuffmanQueue():
    """
    Priority queue of huffman nodes.
    """

    def __init__(self):
        self._list = []

    def push(self, node):
        """
        Inserts node in an position based on its weight.
        """

        for i, cur in enumerate(self._list):
            if node.weight > cur.weight:
                self._list.insert(i, node)
                return

        self._list.append(node)

    def pop(self):
        """
        Returns and deletes the top node.
        """

        return self._list.pop()

    def __len__(self):
        return len(self._list)

def _huffman(text):
    """
    Applies Huffamn coding in text and returns a dict with all characters and
    their respective codes.
    """

    empty_symbol = ""

    queue = HuffmanQueue()

    for symbol in set(text):
        queue.push(HuffmanNode(symbol, text.count(symbol)))

    while len(queue) > 1:
        left = queue.pop()
        right = queue.pop()

        internal = HuffmanNode(empty_symbol, left.weight + right.weight)
        internal.left = left
        internal.right = right

        queue.push(internal)

    return queue.pop().table()

def encode(text):
    """
    Returns a bit-like string representation of text encoded.
    """

    table = _huffman(text)
    encoded_text = "".join(table[symbol] for symbol in text)

    return encoded_text, table

def decode(encoded_text, table):
    """
    Returns the original string.
    """
    codes = sorted(table.items(), key=lambda x: len(x[1]), reverse=True)

    i = 0
    decoded = ""

    while i < len(encoded_text):
        for symbol, code in codes:
            length = len(code)

            if encoded_text[i:i+length] == code:
                decoded += symbol
                i += length
                break

    return decoded

def bytify(encoded_text):
    """
    Returns a bytes object representing the encoded text.
    """

    byte_size = 8
    binary_base = 2

    bytez = []

    for i in range(0, len(encoded_text), byte_size):
        byte = encoded_text[i:i+byte_size]
        bytez.append(byte)

    return bytes(int(byte, binary_base) for byte in bytez)
