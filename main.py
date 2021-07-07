from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_row = {}
word_dict = {}

try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    other_df = pandas.read_csv("data/spanish_words.csv")
    word_dict = other_df.to_dict(orient="records")
else:
    word_dict = df.to_dict(orient="records")


def new_card():
    global current_row, timer
    window.after_cancel(timer)

    current_row = random.choice(word_dict)

    canvas.itemconfig(canvas_image, image=card_front_img)
    canvas.itemconfig(language_text, text="Spanish", fill="black")
    canvas.itemconfig(word_text, text=current_row["Spanish"], fill="black")
    timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_row["English"], fill="white")


def remove_right_answer():
    word_dict.remove(current_row)
    new_df = pandas.DataFrame(word_dict)
    new_df.to_csv("data/words_to_learn.csv", index=False)
    new_card()


# --- UI Setup --- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=1, row=1, columnspan=2)

language_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
new_card()

wrong_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=new_card)
wrong_button.grid(column=1, row=2)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=remove_right_answer)
right_button.grid(column=2, row=2)


window.mainloop()
