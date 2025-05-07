# Accepted characters (pt-br) - used for index translation
ALPHABET = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            'z', 'ç', '-', 'ã', 'á', 'à', 'â', 'é', 'ê', 'í', 'ó', 'õ',
            'ô', 'ú')
# Builds a hashmap            
HASH = {v:k for (k, v) in enumerate(ALPHABET)}
HASH_SIZE = len(HASH)
# Reverse mapping of hash
DECODE = {k:v for (k, v) in enumerate(ALPHABET)}


class Node():
    def __init__(self):
        self.children = [None] * HASH_SIZE
        self.terminal = False


class Trie():
    def __init__(self):
        self.root = Node()
        self.hash = HASH
        self.decode = DECODE

    def insert_word(self, word):
        cur = self.root
        for char in word.lower():
            index = self.hash.get(char)
            try:
                if not cur.children[index]:
                    cur.children[index] = Node()
            except TypeError:
                print(f"-> Unmapper character ({char}) was found in the file.")
                return
            cur = cur.children[index]
        cur.terminal = True
    
    def search_word(self, word):
        cur = self.root
        for char in word:
            index = self.hash.get(char)
            if not cur.children[index]:
                return False
            cur = cur.children[index]
        return cur.terminal

    def search_prefix(self, prefix):
        cur = self.root
        for char in prefix:
            index = self.hash.get(char)
            if not cur.children[index]:
                return False
            cur = cur.children[index]
        return True

    def delete_word(self, word):
        stack = self._build_stack(self.root, word)
        index, node, branches = stack.pop()
        if node.terminal and branches > 0:
            node.terminal = False
            return
        elif node.terminal and branches == 0:
            del(node)
        while stack:
            index, node, branches = stack.pop()
            if node.terminal:
                node.children[index] = None
                return
            if not node.terminal and branches == 1:
                del(node)
            elif not node.terminal and branches > 1:
                node.children[index] = None
                return

    def print_words(self):
        def _traverse(node, prefix=""):
            if node.terminal:
                print(f"-> {prefix}")
            for i, j in enumerate(node.children):
                if j:
                    _traverse(j, prefix + self.decode.get(i))
        _traverse(self.root)
    
    def save_file(self, file_name):
        def _traverse(node, prefix=""):
            if node.terminal:
                f.write(f"{prefix}\n")
            for i, j in enumerate(node.children):
                if j:
                    _traverse(j, prefix+ self.decode.get(i))
        out_name = f"{file_name}-dict.txt"
        with open(out_name, "w", encoding="utf-8") as f:
            _traverse(self.root)
            print(f"File saved as {out_name}")
    
    def reader(self, file_name):
        def _parse(file):
            try:
                with open(file, encoding="utf-8") as f:
                    for line in f:
                        for word in line.split():
                            yield word
            except FileNotFoundError:
                print(f"Could not find {file}")
                return
        for word in _parse(file_name):
            self.insert_word(word)

    def _build_stack(self, node, word):
        stack, cur = list(), node
        for char in word:
            index = self.hash.get(char)
            stack.append((index, cur, sum(1 for i in cur.children if i is not None)))
            cur = cur.children[index]
        stack.append((None, cur, sum(1 for i in cur.children if i is not None)))
        return stack
