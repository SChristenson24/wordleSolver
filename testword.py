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


def get_user_feedback():
    while True:
        feedback = input("Was the result green (g), yellow (y), gray (r), or 100% sure (s)? ").strip().lower()
        if feedback in ['g', 'y', 'r', 's']:
            return feedback
        else:
            print("Invalid input. Please enter 'g' for green, 'y' for yellow, 'r' for gray, or 's' for 100% sure.")


def update_common_letter(yellow_letters, green_letters, gray_letters, word_list):
    all_letters = [letter for word in word_list for letter in word if letter not in gray_letters]
    if all_letters:
        return max(all_letters, key=all_letters.count)
    return None




def a_star(trie, target_word, yellow_letters, green_letters, gray_letters, first_guess=None):
    open_set = [(0, first_guess if first_guess else "", "")]
    closed_set = set()

    while open_set:
        _, current_word, _ = heapq.heappop(open_set)

        if all(letter in green_letters for letter in target_word):
            return current_word

        if current_word in closed_set:
            continue

        closed_set.add(current_word)

        feedback = None
        if len(current_word) == 1:  # Ask for feedback after the first guess
            feedback = get_user_feedback()
            if feedback == 's':
                return current_word
            elif feedback == 'y':
                yellow_letters.append(current_word)
            elif feedback == 'g':
                green_letters.append(current_word)
            elif feedback == 'r':
                gray_letters.append(current_word)

        # Find the most common letter based on the updated lists
        common_letter = update_common_letter(yellow_letters, green_letters, gray_letters, word_list)

        if feedback is not None and common_letter:
            print("Next guess should include:", common_letter)  # Output the most common letter for the next guess

        if feedback not in ['y', 'g']:  # Proceed only if feedback is not yellow or green
            if common_letter:
                for letter in 'abcdefghijklmnopqrstuvwxyz':
                    neighbor_word = current_word + letter
                    if trie.starts_with(neighbor_word):
                        h = heuristic(neighbor_word, target_word, yellow_letters, green_letters)
                        heapq.heappush(open_set, (h, neighbor_word, current_word))
            else:
                for letter in 'abcdefghijklmnopqrstuvwxyz':
                    neighbor_word = current_word + letter
                    if trie.starts_with(neighbor_word):
                        h = heuristic(neighbor_word, target_word, yellow_letters, green_letters)
                        heapq.heappush(open_set, (h, neighbor_word, current_word))

    return None







word_list = ["apple", "banana", "cherry", "grape", "lemon", "orange"]
yellow_letters = []
green_letters = []
gray_letters = []

trie = Trie()
for word in word_list:
    trie.insert(word)

first_guess = input("Enter your first guess: ").strip().lower()
solution = a_star(trie, first_guess, yellow_letters, green_letters, gray_letters)
if solution:
    print("Solution:", solution)
else:
    print("No solution found.")