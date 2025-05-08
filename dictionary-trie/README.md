# Words Dictionary - Trie

## Tries
[trie-example](https://raw.githubusercontent.com/lucascorumba/study-projects/refs/heads/main/readme-imgs/dictionary-trie/trie.png)
>In this image, the terminal nodes are marked as green. 

## About the Scripts
- `dictionary.py`
    - This script has some logic ensuring correct number of input arguments and trie initialization, but most of it is UI. All of the trie operations use function calls from `utils.py`.
- `utils.py`
    - Here is all the code logic related to the operations on the data structure. The operations implemented for the trie are:
        * Insertion
        * Deletion
        * Search prefix
        * Search words
    It also implements the ability to build a trie based of a `.txt` file, print stored words and save stored words in a `.txt` file.
    The accepted characters are stored in a the `alphabet` hashmap. It can be changed as needed.
- `trie.py`
    - *TODO*

## Requirements
No additional libraries, so no need for `pip` or virtual environments.

## Usage
```py
python3 dictionary.py file.txt
```