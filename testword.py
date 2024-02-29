import heapq


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True


def heuristic(word, target_word, yellow_letters, green_letters):
    yellow_count = sum(1 for letter in word if letter in yellow_letters)
    green_count = sum(1 for letter in word if letter in green_letters)
    total_match = yellow_count + green_count
    incorrect_letters = len(word) - total_match
    incorrect_letters_in_target = sum(1 for letter in target_word if letter not in word)
    return incorrect_letters + incorrect_letters_in_target


def a_star(trie, target_word, yellow_letters, green_letters, gray_letters):
    open_set = [(0, "", "")]  
    closed_set = set()

    while open_set:
        _, current_word, _ = heapq.heappop(open_set)

        if current_word == target_word:
            return current_word

        if current_word in closed_set:
            continue

        closed_set.add(current_word)

        for letter in 'abcdefghijklmnopqrstuvwxyz':
            neighbor_word = current_word + letter
            if trie.starts_with(neighbor_word):
                h = heuristic(neighbor_word, target_word, yellow_letters, green_letters)
                heapq.heappush(open_set, (h, neighbor_word, current_word))

    return None


word_list = ["apple", "banana", "cherry", "grape", "lemon", "orange"]
target_word = "apple"
yellow_letters = ['p', 'l']
green_letters = ['a']
gray_letters = []

trie = Trie()
for word in word_list:
    trie.insert(word)

solution = a_star(trie, target_word, yellow_letters, green_letters, gray_letters)
print("Solution:", solution)
