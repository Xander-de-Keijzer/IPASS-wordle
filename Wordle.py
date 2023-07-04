import tkinter as tk
import random

from tkinter import messagebox
from Data import Result, Filter
from AI import Solver

class Window:
    def __init__(self, columns: int, rows: int, box_size: int, check_function, suggested: list[str]) -> None:
        self.columns = columns + 3
        self.rows = rows
        self.box_size = box_size
        self.window = tk.Tk()
        self.submit = check_function
        self.suggested = suggested
        self.load_window()

    def load_window(self):
        window_width = self.columns * self.box_size + 10
        window_height = self.rows * self.box_size + 120 

        self.window.title("Wordle")
        self.window.configure(bg="#121213")
        self.window.geometry(f"{window_width}x{window_height}")
        
        self.load_labels()

        # Create the instructions label
        self.label_instructions = tk.Label(self.window, text=f"Guess the {self.columns-3}-letter word:", font=("Helvetica", 14), fg="white", bg="#121213")
        self.label_instructions.grid(row=1, column=1, columnspan=self.columns, padx=5, pady=10)

        # Create the submit button
        self.button_submit = tk.Button(self.window, relief="flat", text="Submit", font=("Helvetica", 14), command=self.submit, fg="#ffffff", bg="#818384")
        self.button_submit.grid(row=self.rows+3, column=1, columnspan=self.columns, padx=5, pady=10)

        # Create list of best words
        self.best_word_title = tk.Label(self.window, text=f"Best words:", font=("Helvetica", 14), fg="white", bg="#121213")
        self.best_word_title.grid(row=1, column=self.columns-1, columnspan=self.columns, padx=15, pady=10)

        self.best_words = []
        for i in range(6):
            best_word = tk.Label(self.window, text=self.suggested[i], font=("Helvetica", 14), fg="white", bg="#121213")
            best_word.grid(row=i+2, column=self.columns-1, columnspan=self.columns, padx=15, pady=10)
            self.best_words.append(best_word)

    def load_labels(self):
        self.guess_labels = []
        for row in range(self.rows):
            guess_row = []
            for column in range(self.columns - 3):
                frame = tk.Frame(self.window, highlightthickness=1, highlightbackground="#3a3a3c", borderwidth=1, bg="#121213", width=self.box_size, height=self.box_size)
                frame.grid(row=row+2, column=column+2, padx=3, pady=3)
                label = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), width=2, height=1, fg="white", bg="#1a1a1c")
                label.pack(fill=tk.BOTH, expand=True)
                guess_row.append(label)
            self.guess_labels.append(guess_row)


class Wordle:
    def __init__(self, allowed_guesses: list[str], posible_answers: list[str]) -> None:
        self.solver = Solver(allowed_guesses)
        self.filter = Filter([])
        self.guesses = allowed_guesses
        self.answers = posible_answers
        self.guesses.extend(posible_answers)
        self.target_word = random.choice(self.answers)
        self.rows = 6
        self.window = Window(len(self.target_word), self.rows, 60, self.check_guess, self.solver.best_guesses(self.filter, 6))
        self.guess = [" "] * len(self.target_word)
        self.attempts = 0
        self.current_box = 0

    def start(self):
        self.window.window.bind("<Key>", self.key_press)
        self.window.window.mainloop()

    def key_press(self, event):
        letter = event.char.upper()

        # Update the guess
        if letter.isalpha() and self.current_box < len(self.target_word):
            self.guess[self.current_box] = letter
            self.window.guess_labels[self.attempts][self.current_box].config(text=letter)
            self.current_box += 1
        elif event.keysym == "BackSpace" and self.current_box > 0:
            self.current_box -= 1
            self.guess[self.current_box] = " "
            self.window.guess_labels[self.attempts][self.current_box].config(text=" ")
        elif event.keysym == "Return":
            self.check_guess()

    def check_guess(self):

        user_guess = "".join(self.guess)

        # Validate the guess
        if user_guess not in self.guesses:
            messagebox.showerror("Invalid Guess", "Please enter a valid guess.")
        else:
            self.attempts += 1
            result = Result.from_guess(user_guess, self.target_word)
            self.filter.results.append(result)

            best = self.solver.best_guesses(self.filter, 6)
            for index, label in enumerate(self.window.best_words):
                if index >= len(best):
                    label.config(text="_____")
                else:
                    label.config(text=best[index])

            for index, color in enumerate(result.get_colors()):
                if color == "green":
                    self.window.guess_labels[self.attempts-1][index].config(text=self.guess[index], relief=tk.FLAT, fg="white", bg="#538d4e")  # Green for correct placed letters
                elif color == "yellow":
                    self.window.guess_labels[self.attempts-1][index].config(text=self.guess[index], relief=tk.FLAT, fg="white", bg="#b59f3b")  # Yellow for correct letters in different position
                else:
                    self.window.guess_labels[self.attempts-1][index].config(text=self.guess[index], relief=tk.FLAT, fg="white", bg="#3a3a3c")  # Gray for incorrect letters

            # Check for win or loss
            if self.guess == list(self.target_word):
                messagebox.showinfo("Congratulations!", "You guessed the word correctly!")
                self.window.window.quit()
            elif self.attempts >= self.rows:
                messagebox.showinfo("Game Over", "You have reached the maximum number of attempts.")
                self.window.window.quit()
            else:
                self.current_box = 0
                self.guess = [" "] * len(self.target_word)

def load_data() -> tuple[list[str]]:
    # Read the valid guesses from the file
    with open("wordle-nyt-allowed-guesses.txt", "r") as f:
        valid_guesses = [word.strip().upper() for word in f]

    # Read the valid secret words from the file
    with open("wordle-nyt-answers-alphabetical.txt", "r") as f:
        valid_secret_words = [word.strip().upper() for word in f]

    # All valid secrets word can also be guessed (ofcourse)
    valid_guesses.extend(valid_secret_words)
    return valid_guesses, valid_secret_words


def main():
    valid_guesses, valid_secret_words = load_data()
    wordle = Wordle(valid_guesses, valid_secret_words)
    wordle.start()


if __name__ == "__main__":
    main()
