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
    queue = deque(
        [(trie.root, "", [False] * 5)]
    )  # Initialize with the trie root, empty word, and unused 'correct' flags

    while queue:
        node, word, used_positions = queue.popleft()

        if len(word) == 5:  # Check if the word length is complete
            if node.is_end_of_word:
                # Ensure 'present' letters are in the word, considering their known incorrect positions
                valid = True
                for letter, positions in present.items():
                    if letter not in word or any(
                        used_positions[pos] for pos in positions if pos < len(word)
                    ):
                        valid = False
                        break
                if valid:
                    valid_words.append(word)
            continue

        index = len(word)  # Current position being filled in the word

        if index in correct:  # If a correct letter is specified for this position
            letter = correct[index]
            if (
                letter in node.children
            ):  # Ensure the correct letter is a valid next step
                used_positions_copy = used_positions[:]
                used_positions_copy[index] = True  # Mark this position as used
                queue.append(
                    (node.children[letter], word + letter, used_positions_copy)
                )

        else:  # For positions without a specified correct letter
            for letter, next_node in node.children.items():
                if letter not in absent and not any(
                    index == pos for pos in present.get(letter, [])
                ):  # Check 'absent' and 'present' constraints
                    # Avoid placing 'present' letters in their known incorrect positions
                    queue.append((next_node, word + letter, used_positions))

    return valid_words


#######################
#  Input Placeholder  #
#######################
def get_user_input():
    correct = {}  # {position: letter}
    present = {}  # {letter: [positions]}
    absent = set()  # Set of letters not in the word

    # Correct letters input
    correct_input = input(
        "Enter correct letters with their positions (e.g., 1a 3c), or type 'solved' to end: "
    )
    if correct_input.lower() == "solved":
        return "solved", {}, []  # Early exit if solved

    for entry in correct_input.split():
        if len(entry) == 2:
            position, letter = (
                int(entry[0]) - 1,
                entry[1],
            )  # Adjust for zero-based indexing
            correct[position] = letter

    # Present but incorrectly positioned letters input
    present_input = input(
        "Enter letters known to be in the word with wrong positions (e.g., 1r for 'r' not in position 1): "
    )
    for entry in present_input.split():
        if len(entry) > 1:
            position, letter = int(entry[0]) - 1, entry[1:]
            if letter not in present:
                present[letter] = []
            present[letter].append(position)  # Append incorrect position for the letter

    # Absent letters input
    absent_input = input("Enter letters known not to be in the word: ")
    absent = list(absent_input.replace(" ", ""))

    return correct, present, absent


def update_user_input(correct_positions, incorrect_positions, absent_letters):
    print("\nCurrent guess state:")
    print(f"Correct positions: {correct_positions}")
    print(f"Incorrect positions: {incorrect_positions}")
    print(f"Absent letters: {list(absent_letters)}")

    # Input for correct letters with positions
    while True:
        correct_input = input(
            "Enter correct letter with position (e.g., 1a), or 'done' if no more: "
        )
        if correct_input.lower() == "done":
            break
        if len(correct_input) == 2:
            position, letter = int(correct_input[0]) - 1, correct_input[1]
            correct_positions[position] = letter

    # Input for present letters known to be in the wrong positions
    while True:
        present_input = input(
            "Enter letter known to be in the word with a wrong position (e.g., 1r for 'r' not in position 1), or 'done' if no more: "
        )
        if present_input.lower() == "done":
            break
        if len(present_input) > 1:
            position, letter = int(present_input[0]) - 1, present_input[1:]
            if letter not in incorrect_positions:
                incorrect_positions[letter] = []
            incorrect_positions[letter].append(position)

    # Input for absent letters
    absent_input = input(
        "Enter any new absent letters known not to be in the word (no spaces): "
    )
    for letter in absent_input:
        absent_letters.add(letter)


while True:
    correct, present, absent = get_user_input()

    # Check if the user has indicated that the puzzle was solved
    if correct == "solved":
        print("Puzzle solved! Exiting...")
        break

    # Find words that fit these constraints
    valid_words = bfs_search(trie, correct, present, absent)
    print("Valid words:", valid_words)

    # Optionally, you could add a prompt here to ask if the user wants to continue or has solved the puzzle
    continue_response = input("Continue solving? (y/n): ")
    if continue_response.lower() != "y":
        print("Exiting...")
        break
