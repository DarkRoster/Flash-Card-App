from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flash Card App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# --------------------PANDAS----------------------#

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")


current_card = {}


def get_random_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(on_yuz_resmi, image=front_image)
    canvas.itemconfig(card_title, fill="black")
    canvas.itemconfig(card_word, fill="black")
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_card["French"])
    flip_timer = window.after(3000, change_card_behind)


def change_card_behind():
    canvas.itemconfig(on_yuz_resmi, image=behind_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    get_random_word()


flip_timer = window.after(3000, get_random_word)

canvas = Canvas(width=800, height=526)
front_image = PhotoImage(file="images/card_front.png")
behind_image = PhotoImage(file="images/card_back.png")
on_yuz_resmi = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 100, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image)
unknown_button.config(bg=BACKGROUND_COLOR, highlightthickness=0, relief=SUNKEN, bd=0, command=get_random_word)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image)
known_button.config(bg=BACKGROUND_COLOR, highlightthickness=0, relief=SUNKEN, bd=0, command=is_known)
known_button.grid(row=1, column=1)

get_random_word()

window.mainloop()
