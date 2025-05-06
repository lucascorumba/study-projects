import utils
import sys

# Ensures correct number of arguments
if len(sys.argv) != 2: sys.exit("-> Could not initialize\nUsage: python dictionary.py file.txt")
file_name = sys.argv[1]
print(f"Selected file: {file_name}")


# Initializes root node and inserts words contained in the document into the Trie
root = utils.Node()
for word in utils.reader(file_name):
    utils.insert_word(root, word.lower())


while True:
    command = utils.get_options()
    # Exit
    if command == "7":
        break
    # Save file
    if command == "6":
        utils.save_file(root, file_name)
    # Insert word
    elif command == "5":
        word = input("Word to insert: ")
        utils.insert_word(root, word.lower())
    # Search prefix
    elif command == "4":
        utils.print_result(utils.search_prefix(root, input("Search prefix: ")))
    # Print all words stored in the trie
    elif command == "3":
        print("The dictionary cointains the following words:")
        utils.print_words(root)
    # Delete word
    elif command == "2":
        word = input("Delete word: ")
        if utils.search_word(root, word):
            utils.delete_word(root, word)
            print("Word deleted")
        else: print("Word not in the dictionary")
    # Search word
    elif command == "1":
        utils.print_result(utils.search_word(root, input("Search word: ")))