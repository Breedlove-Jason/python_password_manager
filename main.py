from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [(choice(letters)) for char in range(randint(8, 10))]
    password_symbols = [(choice(symbols)) for char in range(randint(2, 4))]
    password_numbers = [(choice(numbers)) for char in range(randint(2, 4))]

    generated_password = password_letters + password_symbols + password_numbers
    shuffle(generated_password)

    password = "".join(generated_password)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data:
                # Reading old data
                json_data = json.load(data)
                # Updating old data with new data
        except FileNotFoundError:
            print("File not found")
            with open("data.json", mode="w") as data:
                # Saving updated data
                json.dump(new_data, data, indent=4)
        else:
            json_data.update(new_data)
            with open("data.json", mode="w") as data:
                # Saving updated data
                json.dump(json_data, data, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)


# ---------------------------- SEARCH SETUP ------------------------------- #
def search():
    user_input = website_input.get().title()
    try:
        with open("data.json", mode="r") as data:
            json_data = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if user_input in json_data:
            email = json_data[user_input]["email"]
            password = json_data[user_input]["password"]
            messagebox.showinfo(title=user_input, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {user_input} exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
website_input = Entry(width=35)
website_input.focus()
website_input.grid(column=1, row=1, columnspan=2)
search_button = Button(text="Search", width=14, command=search)
search_button.grid(column=2, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_input = Entry(width=35)
email_input.insert(0, "")
email_input.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
password_input = Entry(width=21)
password_input.grid(column=1, row=3, sticky="E")

generate_button = Button(text="Generate Password", width=14, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=40, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
