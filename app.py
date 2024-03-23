from flask import Flask, session, jsonify, request, render_template
import random
from wordleSolve import Trie, populate_trie

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
    # Select a random word from the list of valid words
    session["target_word"] = random.choice(valid_words)
    return jsonify({"message": "Game started"}), 200


@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.json
    guess = data.get("guess", "").lower()
    if "target_word" not in session:
        return jsonify({"error": "Game not started"}), 400
    if not guess:
        return jsonify({"error": "No guess provided"}), 400

    solution = session.get("target_word")
    if not solution:
        # This should not happen if the game is properly started
        return jsonify({"error": "Solution not found"}), 500

    feedback = get_feedback(guess, solution)
    if feedback is None:
        # Safeguard in case feedback calculation fails
        return jsonify({"error": "Feedback generation failed"}), 500

    # Return the feedback as a valid response
    return jsonify(feedback), 200


def get_feedback(guess, solution):
    feedback = ["gray"] * len(guess)  # Default all to 'gray'
    solution_letters_count = {}

    # First, count occurrences of each letter in the solution
    for letter in solution:
        if letter in solution_letters_count:
            solution_letters_count[letter] += 1
        else:
            solution_letters_count[letter] = 1

    # First pass: Check for correct (green) letters
    for i, letter in enumerate(guess):
        if letter == solution[i]:
            feedback[i] = "green"
            solution_letters_count[letter] -= 1

    # Second pass: Check for present (yellow) letters
    for i, letter in enumerate(guess):
        if (
            feedback[i] == "gray"
            and letter in solution_letters_count
            and solution_letters_count[letter] > 0
        ):
            feedback[i] = "yellow"
            solution_letters_count[letter] -= 1

    return feedback

    feedback = get_feedback(guess, solution)
    return jsonify(feedback)


if __name__ == "__main__":
    app.run(debug=True)
