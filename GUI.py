import tkinter as tk
from tkinter import messagebox
import random

# Read the valid guesses from the file
with open("wordle-nyt-allowed-guesses.txt", "r") as f:
    valid_guesses = [word.strip().upper() for word in f]

# Read the valid secret words from the file
with open("wordle-nyt-answers-alphabetical.txt", "r") as f:
    valid_secret_words = [word.strip().upper() for word in f]

# Add valid secret words to valid guesses
valid_guesses.extend(valid_secret_words)

# Select a random secret word from the valid secret words list
target_word = random.choice(valid_secret_words)

guess = [" "] * len(target_word)
max_attempts = 6
attempts = 0
current_box = 0
num_boxes = len(target_word)
box_size = 60

# Create the main window
window = tk.Tk()
window.title("Wordle")

window_width = num_boxes * box_size + 10
window_height = max_attempts * box_size + 120 
window.geometry(f"{window_width}x{window_height}")


# window_width = 300
# window_height = 300

# # Calculate the window position
# screen_width = window.winfo_screenwidth()
# screen_height = window.winfo_screenheight()
# x = (screen_width - window_width) // 2
# y = (screen_height - window_height) // 2
# window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set the background color
window.configure(bg="#121213")

# Initialize the game variables


# Define the function to handle button clicks
def check_guess():
    global attempts
    global guess
    global current_box

    # Get the user's guess
    user_guess = "".join(guess)

    # Validate the guess
    if user_guess not in valid_guesses:
        messagebox.showerror("Invalid Guess", "Please enter a valid guess.")
    else:
        attempts += 1

        # Check the correctness of the guess
        correct_positions = []
        correct_letters = []

        for i in range(len(target_word)):
            if user_guess[i] == target_word[i]:
                correct_positions.append(i)
                guess[i] = user_guess[i]
            elif user_guess[i] in target_word:
                correct_letters.append(i)

        # Update the guess labels
        for i in range(len(target_word)):
            if guess[i] == " ":
                guess_labels[attempts-1][i].config(text=guess[i], relief=tk.SOLID, borderwidth=1, fg="white", bg="#121213")
            elif i in correct_positions:
                guess_labels[attempts-1][i].config(text=guess[i], relief=tk.FLAT, fg="white", bg="#538d4e")  # Green for correct placed letters
            elif i in correct_letters:
                guess_labels[attempts-1][i].config(text=guess[i], relief=tk.FLAT, fg="white", bg="#b59f3b")  # Yellow for correct letters in different position
            else:
                guess_labels[attempts-1][i].config(text=guess[i], relief=tk.FLAT, fg="white", bg="#3a3a3c")  # Gray for incorrect letters

        # Check for win or loss
        if guess == list(target_word):
            messagebox.showinfo("Congratulations!", "You guessed the word correctly!")
            window.quit()
        elif attempts >= max_attempts:
            messagebox.showinfo("Game Over", "You have reached the maximum number of attempts.")
            window.quit()
        else:
            current_box = 0
            guess = [" "] * len(target_word)

# Create the guess labels
guess_labels = []
for row in range(max_attempts):
    guess_row = []
    for i in range(num_boxes):
        frame = tk.Frame(window, highlightthickness=1, highlightbackground="#3a3a3c", borderwidth=1, bg="#121213", width=box_size, height=box_size)
        frame.grid(row=row+2, column=i+1, padx=3, pady=3)
        label = tk.Label(frame, text="", font=("Helvetica", 24, "bold"), width=2, height=1, fg="white", bg="#1a1a1c")
        label.pack(fill=tk.BOTH, expand=True)
        guess_row.append(label)
    guess_labels.append(guess_row)

# Create the instructions label
label_instructions = tk.Label(window, text=f"Guess the {num_boxes}-letter word:", font=("Helvetica", 14), fg="white", bg="#121213")
label_instructions.grid(row=1, column=1, columnspan=num_boxes, padx=5, pady=10)

# Create the submit button
button_submit = tk.Button(window, relief="flat", text="Submit", font=("Helvetica", 14), command=check_guess, fg="#ffffff", bg="#818384")
button_submit.grid(row=max_attempts+3, column=1, columnspan=num_boxes, padx=5, pady=10)

# Create empty rows
empty_row_top = tk.Label(window, text="", bg="#121213")
empty_row_top.grid(row=0)
empty_row_bottom = tk.Label(window, text="", bg="#121213")
empty_row_bottom.grid(row=max_attempts+4)


# Function to handle key press events
def key_press(event):
    global current_box
    global guess

    # Get the pressed key
    letter = event.char.upper()

    # Update the guess
    if letter.isalpha() and current_box < len(target_word):
        guess[current_box] = letter
        guess_labels[attempts][current_box].config(text=letter)
        current_box += 1
    elif event.keysym == "BackSpace" and current_box > 0:
        current_box -= 1
        guess[current_box] = " "
        guess_labels[attempts][current_box].config(text=" ")
    elif event.keysym == "Return":
        check_guess()

# Bind the key press event to the window
window.bind("<Key>", key_press)

# Start the GUI
window.mainloop()
