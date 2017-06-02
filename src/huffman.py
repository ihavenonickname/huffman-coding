"""
Provides top-level functions for encoding and decoding with Huffman method.
"""

from queue import PriorityQueue, Empty

class HuffmanNode():
    """
    Node of a Huffman Tree.
    """

    def __init__(self, data, occurrences):
        self.data = data
        self.occurrences = occurrences
        self.left = None
        self.right = None

    def codes(self, code=""):
        """
        Returns a dict with all characters and their respective codes.
        """

        datum = {}

        if self.data:
            datum[self.data] = code if code else "0"

        if self.left:
            datum.update(self.left.codes(code + "0"))

        if self.right:
            datum.update(self.right.codes(code + "1"))

        return datum

class FrequencyQueue():
    """
    Priority queue of huffman nodes.
    """

    def __init__(self):
        self._list = []

    def push(self, node):
        """
        Inserts node in an position based on its occurrences. Higher
        occurrences on top.
        """

        for i, cur in enumerate(self._list):
            if node.occurrences > cur.occurrences:
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

def huffman(text):
    """
    Applies Huffamn method in text and returns a dict with all characters and
    their respective codes.
    """

    queue = FrequencyQueue()

    for item in set(text):
        queue.push(HuffmanNode(item, text.count(item)))

    while len(queue) > 1:
        left = queue.pop()
        right = queue.pop()

        internal = HuffmanNode("", left.occurrences + right.occurrences)
        internal.left = left
        internal.right = right

        queue.push(internal)

    return queue.pop().codes()

def stringify(text, codes):
    """
    Returns a bit-like string representation of text encoded with codes.
    """

    return "".join(codes[c] for c in text)

def bytify(text, codes):
    """
    Returns a bytes object representing text encoded with codes.
    """

    byte_size = 8
    binary_base = 2

    bytez = []

    bits = stringify(text, codes)

    for i in range(0, len(bits), byte_size):
        bytez.append(bits[i:i+byte_size])

    return bytes(int(byte, binary_base) for byte in bytez)
