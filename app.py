from flask import Flask, session, jsonify, request, render_template
import random
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


@app.route("/check_guess", methods=["POST"])
def check_guess():
    data = request.json
    guess = data.get("guess", "").lower()
    print(f"Received guess: {guess}")

    if "target_word" not in session:
        return jsonify({"error": "Game not started"}), 400

    if not guess or guess not in valid_words:
        return jsonify({"error": "Word does not exist in dictionary"}), 400

    solution = session.get("target_word")
    feedback = get_feedback(guess, solution)
    print(f"Feedback: {feedback}")
    session["guesses"].append((guess, feedback))

    # Retrieve and update the absent set
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
            absent.add(guess[i])

    # Store the updated absent set
    session["absent_letters"] = list(absent)

    print("Feedback for guess:", feedback)
    print("Correct:", correct)
    print("Present:", present)
    print("Absent:", absent)

    possible_solutions = bfs_search(trie, correct, present, absent)
    print(f"Possible solutions: {possible_solutions}")
    print("Possible solutions found:", possible_solutions)

    game_over = all(f == "green" for f in feedback)
    if game_over:
        session.pop("target_word", None)
        session.pop("absent_letters", None)  # Also clear the absent letters
        return (
            jsonify(
                {"feedback": feedback, "game_over": True, "message": "Congratulations!"}
            ),
            200,
        )

    return (
        jsonify(
            {
                "feedback": feedback,
                "game_over": False,
                "possible_solutions": possible_solutions,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
