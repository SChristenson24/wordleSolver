from flask import Flask, session, jsonify, request, render_template
import random
from collections import Counter
from wordleSolve import Trie, populate_trie, bfs_search

app = Flask(__name__)
app.secret_key = "your_secret_key"

trie = Trie()
dictionary_path = "dictionary.txt"
populate_trie(trie, dictionary_path)


@app.route("/")
def index():
    return render_template("index.html")


# Assuming you have a list of valid target words loaded into 'valid_words'
with open(dictionary_path) as f:
    valid_words = [word.strip() for word in f.readlines() if len(word.strip()) == 5]


@app.route("/start_game", methods=["GET"])
def start_game():
    session["target_word"] = random.choice(valid_words)
    session["guesses"] = []
    session["absent_letters"] = []  # Store as an empty list instead of a set
    return jsonify({"message": "Game started"}), 200


def get_feedback(guess, solution):
    feedback = ["gray"] * len(guess)  # Default all to 'gray'
    solution_letters_count = Counter(
        solution
    )  # Use collections.Counter to simplify counting

    # First pass: Check for correct (green) letters and remove from count
    for i, letter in enumerate(guess):
        if letter == solution[i]:
            feedback[i] = "green"
            solution_letters_count[letter] -= 1

    # Second pass: Check for present (yellow) letters and adjust the count accordingly
    for i, letter in enumerate(guess):
        if feedback[i] == "gray" and solution_letters_count[letter] > 0:
            feedback[i] = "yellow"
            solution_letters_count[letter] -= 1

    # Third pass: Adjust feedback for gray letters only if they exceed the count in the solution
    for i, letter in enumerate(guess):
        if feedback[i] == "gray" and guess.count(letter) > solution.count(letter):
            feedback[i] = (
                "gray"  # Actually unnecessary since it's default, but here for clarity
            )

    return feedback


@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.json
    guess = data.get("guess", "").lower()
    print(f"Received guess: {guess}")

    if "target_word" not in session:
        return jsonify({"error": "Game not started"}), 400
    
    target_word = session.get("target_word")

    if not guess or guess not in valid_words:
        return jsonify({"error": "Word does not exist in dictionary"}), 400

    solution = session.get("target_word")
    feedback = get_feedback(guess, solution)
    session["guesses"].append((guess, feedback))

    # Retrieve the current absent letters from the session
    absent = set(session.get("absent_letters", []))
    correct, present = {}, {}

    for i, f in enumerate(feedback):
        if f == "green":
            correct[i] = guess[i]
        elif f == "yellow":
            if guess[i] not in present:
                present[guess[i]] = []
            present[guess[i]].append(i)
        elif f == "gray":
            # The letter should be added to absent only if it's not in the correct or present
            if guess[i] not in correct.values() and not any(
                guess[i] in pos for pos in present.values()
            ):
                absent.add(guess[i])

    # Store the updated absent set, making sure to convert it back to a list
    session["absent_letters"] = list(absent)

    # Calculate the possible solutions with the current feedback
    possible_solutions = bfs_search(trie, correct, present, absent)
    print(f"Possible solutions: {possible_solutions}")

    # Check if the game is over
    game_over = all(f == "green" for f in feedback)
    if game_over:
        # Include the target_word in the JSON response
        return jsonify({
            "feedback": feedback, 
            "game_over": True, 
            "message": "Congratulations!",
            "target_word": target_word  # Add this line
        }), 200
    else:
        # Also include the target word in the response for a non-game-over scenario if needed
        return jsonify({
            "feedback": feedback, 
            "game_over": False, 
            "possible_solutions": possible_solutions,
            "target_word": target_word  # Add this line
        }), 200


if __name__ == "__main__":
    app.run(debug=True)
