import random
import os

# ----------------------------
# WORD CATEGORIES
# ----------------------------
categories = {
    "Fruits": ["apple", "banana", "mango", "orange", "grapes"],
    "Countries": ["india", "canada", "japan", "brazil", "germany"],
    "Programming": ["python", "variable", "function", "compiler", "algorithm"]
}

# ----------------------------
# HANGMAN STAGES
# ----------------------------
hangman_stages = [
    """
     -----
     |   |
         |
         |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
         |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
     |   |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|   |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
         |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    =========
    """
]


# ----------------------------
# HIGH SCORE FUNCTIONS
# ----------------------------
def save_score(name, score):
    with open("highscores.txt", "a") as file:
        file.write(f"{name}:{score}\n")


def show_leaderboard():
    print("\n===== LEADERBOARD =====")

    if not os.path.exists("highscores.txt"):
        print("No scores yet.")
        return

    scores = []

    with open("highscores.txt", "r") as file:
        for line in file:
            try:
                name, score = line.strip().split(":")
                scores.append((name, int(score)))
            except:
                pass

    scores.sort(key=lambda x: x[1], reverse=True)

    for i, (name, score) in enumerate(scores[:10], start=1):
        print(f"{i}. {name} - {score}")

    print("=======================\n")


# ----------------------------
# MAIN GAME FUNCTION
# ----------------------------
def play_game():

    print("\nChoose Difficulty")
    print("1. Easy (8 lives)")
    print("2. Medium (6 lives)")
    print("3. Hard (4 lives)")

    difficulty = input("Enter choice: ")

    if difficulty == "1":
        max_wrong = 8
    elif difficulty == "3":
        max_wrong = 4
    else:
        max_wrong = 6

    category = random.choice(list(categories.keys()))
    word = random.choice(categories[category])

    guessed_word = ["_"] * len(word)
    guessed_letters = set()

    wrong_guesses = 0
    hint_used = False

    print(f"\nCategory: {category}")

    while wrong_guesses < max_wrong and "_" in guessed_word:

        print("\n" + hangman_stages[min(wrong_guesses, 6)])
        print("Word:", " ".join(guessed_word))

        if guessed_letters:
            print("Guessed Letters:", ", ".join(sorted(guessed_letters)))

        print(f"Lives Remaining: {max_wrong - wrong_guesses}")
        print("Enter ? for a hint")

        guess = input("Your Guess: ").lower().strip()

        # Hint
        if guess == "?":

            if hint_used:
                print("You already used your hint!")
                continue

            for letter in word:
                if letter not in guessed_word:
                    print(f"Hint: The word contains '{letter}'")
                    hint_used = True
                    break

            continue

        # Validation
        if len(guess) != 1 or not guess.isalpha():
            print("Enter exactly one letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        # Correct Guess
        if guess in word:
            print("Correct!")

            for i in range(len(word)):
                if word[i] == guess:
                    guessed_word[i] = guess

        # Wrong Guess
        else:
            print("Wrong!")
            wrong_guesses += 1

    # ----------------------------
    # GAME RESULT
    # ----------------------------
    if "_" not in guessed_word:

        score = (max_wrong - wrong_guesses) * 10

        print("\n🎉 CONGRATULATIONS! 🎉")
        print("Word:", word)
        print("Score:", score)

        return score

    else:

        print(hangman_stages[6])

        print("\nGAME OVER")
        print("The word was:", word)

        return 0


# ----------------------------
# PROGRAM START
# ----------------------------
print("================================")
print(" HANGMAN GAME")
print("================================")

player_name = input("Enter your name: ").strip()

show_leaderboard()

total_score = 0

while True:

    score = play_game()
    total_score += score

    save_score(player_name, score)

    again = input("\nPlay Again? (Y/N): ").lower()

    if again != "y":
        break

print("\nThanks for playing!")
print("Final Score:", total_score)

show_leaderboard()