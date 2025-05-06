import sys
# Accepted characters (pt-br) - used for index translation
alphabet = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            'z', 'ç', '-', 'ã', 'á', 'à', 'â', 'é', 'ê', 'í', 'ó', 'õ',
            'ô', 'ú')
# Builds a hashmap            
#hash = {k:v for (k, v) in zip(alphabet, range(len(alphabet)))}
hash = {v:k for (k, v) in enumerate(alphabet)}
hash_size = len(hash)
# Reverse mapping of hash
decode = {k:v for (k, v) in enumerate(alphabet)}


class Node():
    def __init__(self):
        self.elements = [None] * hash_size
        self.terminal = False



def insert_word(root, word):
    """
    Inserts new word into the trie. Only accepts characters contained in 'alphabet'
    """
    # Set cursor pointing to root node
    cur = root

    # iterates over every character of the word
    for char in word.lower():
        # Uses hashmap to get character index
        index = hash.get(char)
        try:
            # Triggers if current char is not yet in the list
            if not cur.elements[index]:
                # Points current node[index] to new node
                cur.elements[index] = Node()
        # Triggers if 'index' value is None -> char not in alphabet
        except TypeError:
            sys.exit(f"-> Unmapped character ({char}) was found in the file. \
            \nRun 'python utils.py' to see all mapped characters")
        # Moves the cursor to next node or new node
        cur = cur.elements[index]
    # Marks last node as a terminal node (end of the word)
    #cur.set_terminal()
    cur.terminal = True


def search_word(root, word):
    """
    Takes root node and lookup word as input.
    Returns True if word is ontained in the trie, False otherwise.
    """
    # Initializes cursor
    cur = root
    for char in word:
        index = hash.get(char)
        # If hash result leads to empty node -> word is not in the trie
        if not cur.elements[index]:
            return False
        cur = cur.elements[index]
    # Returns last node value for terminal marker
    return cur.terminal


def search_prefix(root, prefix):
    """
    Takes root node and prefix as input.
    Returns True if prefix is found in the trie, and False otherwise.
    """
    cur = root
    for char in prefix:
        index = hash.get(char)
        # If hash result leads to empty node -> prefix is not in the trie
        if not cur.elements[index]:
            return False
        cur = cur.elements[index]
    # If the code reached this point, the prefix is in the trie
    return True


def build_stack(node, word):
    """
    Traverse the trie until end of the word is reached.
    Adds every node to a stack. Returns stack once terminal node is reached.
    Used by 'delete_words()'.
    """
    stack, cur = list(), node
    for char in word:
        index = hash.get(char)
        stack.append((index, cur, sum(1 for i in cur.elements if i is not None)))
        cur = cur.elements[index]
    stack.append((None, cur, sum(1 for i in cur.elements if i is not None)))
    return stack    


def delete_word(root, word):
    """
    Takes root node and word to be deleted as input.
    Deletes or alters nodes without breaking references to other stored words.
    Assumes the provided word is contained in the trie -- relies on external call of 'search_word()'.
    """
    # Builds stack based on provided word
    stack = build_stack(root, word)

    # Gets current word's terminal node
    index, node, branches = stack.pop()
    # Resolves action over terminal node 
    if node.terminal and branches > 0:
        node.terminal = False
        return
    elif node.terminal and branches == 0:
        del(node)

    # Resolve following characters
    while stack:
        index, node, branches = stack.pop()
        if node.terminal:
            node.elements[index] = None
            return
        if not node.terminal and branches == 1:
            del(node)
        elif not node.terminal and branches > 1:
            node.elements[index] = None
            return


def print_words(node, prefix=""):
    """
    Receives a trie node and a string prefix as input. Assumes node = root.
    Runs through the entire trie and prints all words found.
    """
    # When terminal node is found, prints accumulated chars
    if node.terminal:
        print(f"-> {prefix}")

    # j are node references
    for i, j in enumerate(node.elements):
        if j:
            # Recursively adds chars to prefix
            print_words(j, prefix + decode.get(i))


def save_file(root, file_name):
    """
    Writes stored words in a .txt file
    """
    # Traverse the trie exactly like 'print_words()'
    def traverse(node, prefix=""):
        if node.terminal:
            f.write(f"{prefix}\n")
        for i, j in enumerate(node.elements):
            if j:
                traverse(j, prefix + decode.get(i))

    # Produces name for the new file
    out_name = f"{file_name.split('.')[0]}-dict.txt"
    with open(out_name, "w", encoding="utf-8") as f:       
        traverse(root)
        print(f"File saved as {out_name}")
            

def reader(file_name):
    """
    Open text file in read mode and yield one word at a time.
    """
    try:
        with open(file_name, encoding="utf-8") as f:
            for line in f:
                for word in line.split():
                    yield word
    except FileNotFoundError:
        sys.exit(f"Could not find {file_name}")


def get_options():
    """
    Prompts user for input and ensure that provided option is valid.
    Current accepted options: 
    (1)Search, (2)Delete, (3)Print words, (4)Search prefix, 
    (5)Insert Word, (6)Save File, (7)Exit 
    """
    options = ("1", "2", "3", "4", "5", "6", "7")
    while True:
        print("Select an option:\
            \n\t1- Search Word\n\t2- Delete Word\n\t3- Print Stored Words\
            \n\t4- Search Prefix\n\t5- Insert Word\n\t6- Save File\n\t7- Exit")
        
        command = input()    
        if command not in options:
            print("Command not found plese input a option number (1, 2, 3, 4 or 5)\n")
            continue
        else:
            return command


def print_result(bool):
    """
    Takes in a boolean value and prints messages for each case
    """
    if bool: print("Found")
    else: print("Not found")
    print()


if __name__ == "__main__":
    print(f"Alphabet size: {len(alphabet)} characters\n{alphabet}")
    