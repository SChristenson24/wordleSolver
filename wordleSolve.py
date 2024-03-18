from collections import deque


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
    queue = deque([(trie.root, "", [False] * 5)])

    while queue:
        node, word, used_positions = queue.popleft()
        if len(word) == 5 and node.is_end_of_word:
            if all(letter in word for letter in present.keys()):
                valid_words.append(word)
            continue

        if len(word) < 5:
            for letter, next_node in node.children.items():
                if letter in absent or (
                    letter in present and len(word) in present[letter]
                ):
                    continue
                new_used_positions = used_positions[:]
                if len(word) in correct and correct[len(word)] == letter:
                    new_used_positions[len(word)] = True
                    queue.append((next_node, word + letter, new_used_positions))
                elif len(word) not in correct:
                    queue.append((next_node, word + letter, new_used_positions))

    return valid_words


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
