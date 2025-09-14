import os
import pandas
import random
import tkinter

BACKGROUND_COLOR = "#B1DDC6"
#------------------------------NEW FLASHCARDS------------------------------
try:
    with open("./data/words_to_learn.csv", mode="r", encoding="utf-8") as f:
        dictionary = pandas.read_csv(f).to_dict(orient="records")
except FileNotFoundError:
    dictionary = pandas.read_csv("./data/french_words.csv", encoding="utf-8").to_dict(orient="records")

word = {}

def change_cards() -> None:
    global word, flip
    word = random.choice(dictionary)
    canvas.itemconfig(canvas_image, image=card)
    canvas.itemconfig(language_label, text="French", fill="black")
    canvas.itemconfig(word_label, text=word['French'], fill="black")
    flip = window.after(3000, flipping)

def random_picking() -> None:
    if dictionary:
        if flip is not None:
            window.after_cancel(flip)
        change_cards()

def flipping() -> None:
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(language_label, text="English", fill="white")
    canvas.itemconfig(word_label, text=word['English'], fill="white")

def is_known() -> None:
    global word, dictionary, flip
    if flip is not None:
        window.after_cancel(flip)

    if not dictionary:
        canvas.itemconfig(canvas_image, image=card_back)
        canvas.itemconfig(language_label, text="All done", fill="white")
        canvas.itemconfig(word_label, text="Congratulations!", fill="white")
    else:
        dictionary.remove(word)
        pandas.DataFrame(dictionary).to_csv("./data/words_to_learn.csv", index=False)

        if dictionary:
            change_cards()
        else:
            os.remove("./data/words_to_learn.csv")

#------------------------------UI INTERFACE------------------------------
window = tkinter.Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip = None

canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = tkinter.PhotoImage(file="./images/card_front.png")
canvas_image = canvas.create_image(400, 263, image=card)
language_label = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"), fill="black")
word_label = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"), fill="black")
card_back = tkinter.PhotoImage(file="./images/card_back.png")
canvas.grid(row=0, column=0, columnspan=2)

red_image = tkinter.PhotoImage(file="./images/wrong.png")
green_image = tkinter.PhotoImage(file="./images/right.png")

red_button = tkinter.Button(image=red_image, highlightthickness=0, command=random_picking)
red_button.grid(row=1, column=0)

green_button = tkinter.Button(image=green_image, highlightthickness=0, command=is_known)
green_button.grid(row=1, column=1)

random_picking()

window.mainloop()