from collections import deque


#######################
#        Trie         #
#######################
class TrieNode:
    def __init__(self):
        self.children = (
            {}
        )  # this is initializing the dictionary that we will populate with Dictionary.txt later
        self.is_end_of_word = False  # this is to check if a node is the end of a word


class Trie:
    def __init__(self):
        self.root = TrieNode()  # root (beginning of trie)

    def insert(self, word):  # insert node into trie
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()  # if not found add a new node
            node = node.children[char]  # put chars into children node
        node.is_end_of_word = True  # mark last node as end


def populate_trie_from_dictionary(trie, dictionary_path):
    with open(dictionary_path, "r") as dictionary_file:  # dictionary fh
        for line in dictionary_file:
            word = (
                line.strip().lower()
            )  # remove newline characters and convert to lowercase
            trie.insert(word)


# create an instance of the Trie
trie = Trie()

dictionary_path = "Dictionary.txt"

# populate the trie with words from the dictionary
populate_trie_from_dictionary(trie, dictionary_path)


#######################
#         BFS         #
#######################
def bfs_search(trie, correct, present, absent):
    valid_words = []
    queue = deque([(trie.root, "", 0)])  # node, current word, and index

    while queue:
        node, word, index = queue.popleft()

        # final word checks
        if len(word) == 5:
            if node.is_end_of_word:
                # ensure 'present' letters are in the word
                if all(letter in word for letter in present):
                    valid_words.append(word)
            continue

        # apply 'correct' constraint
        if index in correct:
            letter = correct[index]
            if letter in node.children:
                queue.append((node.children[letter], word + letter, index + 1))

        # apply 'absent' and 'present' constraints
        else:
            for letter, next_node in node.children.items():
                if letter not in absent and (
                    not index in correct or correct[index] != letter
                ):
                    queue.append((next_node, word + letter, index + 1))

    return valid_words


#######################
#  Input Placeholder  #
#######################
correct = {1: "a"}
present = ["r"]
absent = ["s", "t", "e"]

valid_words = bfs_search(trie, correct, present, absent)
print("Valid words:", valid_words)
