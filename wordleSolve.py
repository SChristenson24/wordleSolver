from collections import deque

# Dictionary from https://gist.github.com/shmookey/b28e342e1b1756c4700f42f17102c2ff


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
            node = node.children.setdefault(char, TrieNode())
        node.is_end_of_word = True


def populate_trie(trie, dictionary_path):
    with open(dictionary_path, "r") as file:
        for word in file:
            trie.insert(word.strip().lower())


def bfs_search(trie, correct, present, absent):
    valid_words = []
    queue = deque([(trie.root, "", 0)])  # Start with the Trie root, an empty word, and a length of 0.

    while queue:
        node, word, length = queue.popleft()

        # When a word reaches the desired length of 5, check if it's valid.
        if length == 5:
            if node.is_end_of_word and is_word_valid(word, correct, present, absent):
                valid_words.append(word)
            continue

        if length >= 5:
            continue  # Skip if the word is already at maximum length.

        # Generate potential next steps.
        for letter, next_node in node.children.items():
            # Check if the next letter should be added to the word.
            if should_skip_letter(letter, length, correct, present, absent, word):
                continue

            queue.append((next_node, word + letter, length + 1))

    return valid_words

def is_word_valid(word, correct, present, absent):
    # Check correct letter positions
    for pos, char in correct.items():
        if word[pos] != char:
            return False

    letter_count = {char: word.count(char) for char in set(word)}

    # Ensure letters marked as present but in wrong positions are correctly counted
    for char, positions in present.items():
        if letter_count.get(char, 0) < 1:
            return False

    # Absent letters should not appear outside allowed occurrences
    for char in absent:
        if char in letter_count and char not in present and char not in correct.values():
            return False

    return True

def should_skip_letter(letter, position, correct, present, absent, word):
    if letter in absent and letter not in present and letter not in correct.values():
        return True

    if position in correct and correct[position] != letter:
        return True

    # Incorrect positions for letters marked as present
    if letter in present and position in present[letter]:
        return True

    return False


def get_user_input(incorrect_positions, absent_letters):
    print("\nIncorrect positions so far: {}".format(incorrect_positions))
    print(
        "Absent letters so far: {}".format(
            ", ".join(absent_letters) if absent_letters else "None"
        )
    )

    correct = {}
    present = incorrect_positions
    absent = absent_letters

    # Correct letters input
    correct_input = input(
        "Enter correct letters with their positions (e.g., 1a 3c), or type 'solved' to end: "
    )
    if correct_input.lower() == "solved":
        return "solved", present, absent

    for entry in correct_input.split():
        if len(entry) >= 2 and entry[0].isdigit():
            position, letter = int(entry[0]) - 1, entry[1:]
            correct[position] = letter

    present_input = input(
        "Enter new letters known to be in the word with wrong positions (e.g., 1r): "
    )
    for entry in present_input.split():
        if len(entry) > 1 and entry[0].isdigit():
            position, letter = int(entry[0]) - 1, entry[1:]
            if letter not in present:
                present[letter] = []
            present[letter].append(position)
        else:
            print(
                "Invalid input. Please enter a position followed by a letter (e.g., 1r)."
            )

    absent_input = input("Enter any new absent letters not in the word (no spaces): ")
    for letter in absent_input:
        if letter.isalpha():
            absent.add(letter)

    return correct, present, absent


def main():
    trie = Trie()
    dictionary_path = "Dictionary.txt"
    populate_trie(trie, dictionary_path)

    incorrect_positions = {}
    absent_letters = set()

    while True:
        correct, present, absent = get_user_input(incorrect_positions, absent_letters)
        if correct == "solved":
            print("Puzzle solved! Exiting...")
            break

        valid_words = bfs_search(trie, correct, present, absent)
        print("Valid words:", valid_words)

        if input("Continue solving? (y/n): ").lower() != "y":
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
