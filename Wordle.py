import tkinter as tk
import random

from tkinter import messagebox

class Window:
    def __init__(self, columns: int, rows: int, box_size: int, check_function) -> None:
        self.columns = columns
        self.rows = rows
        self.box_size = box_size
        self.window = tk.Tk()
        self.submit = check_function
        self.load()

    def load(self):
        window_width = self.columns * self.box_size + 10
        window_height = self.rows * self.box_size + 120 

        self.window.title("Wordle")
        self.window.configure(bg="#121213")
        self.window.geometry(f"{window_width}x{window_height}")
        
        self.load_labels()

        # Create the instructions label
        self.label_instructions = tk.Label(self.window, text=f"Guess the {self.columns}-letter word:", font=("Helvetica", 14), fg="white", bg="#121213")
        self.label_instructions.grid(row=1, column=1, columnspan=self.columns, padx=5, pady=10)

        # Create the submit button
        self.button_submit = tk.Button(self.window, relief="flat", text="Submit", font=("Helvetica", 14), command=self.submit, fg="#ffffff", bg="#818384")
        self.button_submit.grid(row=self.rows+3, column=1, columnspan=self.columns, padx=5, pady=10)

        # Create empty rows
        self.empty_row_top = tk.Label(self.window, text="", bg="#121213")
        self.empty_row_top.grid(row=0)
        self.empty_row_bottom = tk.Label(self.window, text="", bg="#121213")
        self.empty_row_bottom.grid(row=self.rows+4)

    def load_labels(self):
        self.guess_labels = []
        for row in range(self.rows):
            guess_row = []
            for i in range(self.columns):
                frame = tk.Frame(self.window, highlightthickness=1, highlightbackground="#3a3a3c", borderwidth=1, bg="#121213", width=self.box_size, height=self.box_size)
                frame.grid(row=row+2, column=i+1, padx=3, pady=3)
                label = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), width=2, height=1, fg="white", bg="#1a1a1c")
                label.pack(fill=tk.BOTH, expand=True)
                guess_row.append(label)
            self.guess_labels.append(guess_row)

class Wordle:
    def __init__(self, guesses: list[str], answers: list[str]) -> None:
        self.guesses = guesses
        self.answers = answers
        self.guesses.extend(answers)
        self.target_word = random.choice(self.answers)
        self.rows = 6
        self.window = Window(len(self.target_word), self.rows, 60, self.check_guess)
        self.guess = [" "] * len(self.target_word)
        self.attempts = 0
        self.current_box = 0

        print(self.target_word)

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

            # Check the correctness of the guess
            correct_positions = []
            correct_letters = []
            letter_counts = {}

            for i in range(len(self.target_word)):

                if user_guess[i] == self.target_word[i]:
                    correct_positions.append(i)
                    self.guess[i] = user_guess[i]
                    if user_guess[i] in letter_counts:
                        letter_counts[user_guess[i]] += 1
                    else:
                        letter_counts[user_guess[i]] = 1
                else:
                    contains = user_guess[i] in self.target_word
                    not_visit = user_guess[i] not in letter_counts or letter_counts[user_guess[i]] < self.target_word.count(user_guess[i])
                    if contains and not_visit:
                        correct_letters.append(i)
                        if user_guess[i] in letter_counts:
                            letter_counts[user_guess[i]] += 1
                        else:
                            letter_counts[user_guess[i]] = 1

            # Update the guess labels
            for i in range(len(self.target_word)):
                if self.guess[i] == " ":
                    self.window.guess_labels[self.attempts-1][i].config(text=self.guess[i], relief=tk.SOLID, borderwidth=1, fg="white", bg="#121213")
                elif i in correct_positions:
                    self.window.guess_labels[self.attempts-1][i].config(text=self.guess[i], relief=tk.FLAT, fg="white", bg="#538d4e")  # Green for correct placed letters
                elif i in correct_letters:
                    self.window.guess_labels[self.attempts-1][i].config(text=self.guess[i], relief=tk.FLAT, fg="white", bg="#b59f3b")  # Yellow for correct letters in different position
                else:
                    self.window.guess_labels[self.attempts-1][i].config(text=self.guess[i], relief=tk.FLAT, fg="white", bg="#3a3a3c")  # Gray for incorrect letters

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

# Read the valid guesses from the file
with open("wordle-nyt-allowed-guesses.txt", "r") as f:
    valid_guesses = [word.strip().upper() for word in f]

# Read the valid secret words from the file
with open("wordle-nyt-answers-alphabetical.txt", "r") as f:
    valid_secret_words = [word.strip().upper() for word in f]

# Add valid secret words to valid guesses
valid_guesses.extend(valid_secret_words)

wordle = Wordle(valid_guesses, valid_secret_words)
wordle.start()
