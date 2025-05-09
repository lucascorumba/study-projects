# Words Dictionary - Trie

## Tries
Tries (also known as **prefix trees**) are tree-like data structures that dynamically stores sets of characters. It enables highly efficient retrieval operations, even in large datasets. 
In a trie, each node represents a single character in a string, as well as paths to the next nodes. The path from the root to a given node represents a **prefix** of one or more stored strings. Nodes do not store any characters pe se, instead each element's **position** within the node determines its associated key.

Each node has as many elements as mapped characters. When a given elements is empty, it means this particular character is not present in the dataset. Likewise, when a node's element points to another node, it represents a mapped character. In this manner, following nodes can tell us if a string is present (or not) in a dataset. 
If the search for a prefix leads to a dead end, it means this particular prefix is not present in the dataset.
In addition, each node can hold a `terminal` state, meaning it is marking the end of a string. With that, the prefix lookup can be extended for whole words.

The below image illustrates a trie storing the strings *"ABC"*, *"ABCD"*, *"ACT"*, *"C"* and *"DO"*.

![trie-example](https://raw.githubusercontent.com/lucascorumba/study-projects/refs/heads/main/readme-imgs/dictionary-trie/trie.png)

>Terminal nodes are marked as green. 


## About the Scripts
* `dictionary.py`
    This script has some logic ensuring correct number of input arguments and trie initialization, but most of it is UI. All of the trie operations use function calls from `utils.py`.
* `utils.py`
    Here is all the code logic related to the operations on the data structure. The operations implemented for the trie are:
        * Insertion
        * Deletion
        * Search prefix
        * Search words
    
    It also implements the ability to build a trie based of a `.txt` file, print stored words and save stored words in a `.txt` file.
    The accepted characters are stored in a the `alphabet` hashmap. It can be changed as needed.
* `trie.py`
    This file encapsulates all the functionalities of `utils.py` in a single class `Trie`. I wasn't planning in doing this, but it seemed appropriate to do so. As it's a later addition, `dictionary.py` does not make use of it.
    The class has the following methods:
    * `insert_word(word)`
    * `search_word(word)`
    * `search_prefix(prefix)`
    * `delete_word(word)`
    * `print_words()`
    * `save_file(file_name)`
    * `reader(file_name)`

## Requirements
No additional libraries, so no need for `pip` or virtual environments.

## Usage
```py
python3 dictionary.py file.txt
```