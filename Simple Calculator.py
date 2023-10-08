import math
import tkinter as tk
import math


# Function to remove a character(s)
def remove_character():

    display_characters = entered_characters.get(1.0, "end")

    text = entered_characters.get(1.0, "end").strip()[-5:]

    # Remove all characters if there is the answer
    if '=' in display_characters:
        clear_text()
    # Remove the whole of a trig function
    elif text == "sin (" or text == "cos (" or text == "tan (":
        display_characters = entered_characters.get(1.0, "end").strip()[:-5]
        clear_text()
        entered_characters.insert(1.0, display_characters)
    # Remove one character at a time if not in any of above modes
    else:
        display_characters = entered_characters.get(1.0, "end").strip()[:-1]
        clear_text()
        entered_characters.insert(1.0, display_characters)


# Function that display the entered characters
def display_text(character):

    display_characters = entered_characters.get(1.0, "end").strip()

    # If there is  the answer extract only the answer and add the entered character
    if '=' in display_characters:
        display_characters = entered_characters.get(2.0, "end").strip()
        display_characters = (display_characters.strip()[1:] + character)
    # Just add the entered character if there is no answer
    else:
        display_characters += character

    clear_text()
    entered_characters.insert(1.0, display_characters)


# Function to remove all characters
def clear_text():
    entered_characters.delete(1.0, "end")


# Function for displaying the answer, i.e, function for the '=' button
def answer():

    display_characters = entered_characters.get(1.0, "end")
    expression = display_characters

    try:
        while "sin" in display_characters or "cos" in display_characters or "tan" in display_characters:
            if "sin" in expression:
                # Finding the first index where 'sin' is found
                first_index = expression.index("sin") + 5
                # Finding index where the sin function ends
                second_index = expression[first_index:].index(")") + len(expression[:first_index])
                # Extracting the degree (Parameter for sin)
                degree = expression[first_index:second_index]
                result = math.sin(float(degree))
                # Updating the expression by replacing the sin function with its return value
                expression = expression.replace(f"sin ({degree})", str(result))

            elif "cos" in expression:
                first_index = expression.index("cos") + 5
                second_index = expression[first_index:].index(")") + len(expression[:first_index])
                degree = expression[first_index:second_index]
                result = math.cos(float(degree))
                expression = expression.replace(f"cos ({degree})", str(result))

            elif "tan" in expression:
                first_index = expression.index("tan") + 5
                second_index = expression[first_index:].index(")") + len(expression[:first_index])
                degree = expression[first_index:second_index]
                result = math.tan(float(degree))
                expression = expression.replace(f"tan ({degree})", str(result))
            else:
                break

        # Evaluate the expression and insert it on the screen
        result = str(eval(expression))
        entered_characters.delete(1.0, "end")
        if len(display_characters) >= 15:
            display_characters = display_characters[:15]
        entered_characters.insert(1.0, f"{display_characters.strip()}\n={result}")

    except (SyntaxError, ZeroDivisionError, TypeError, ValueError):
        clear_text()
        entered_characters.insert(1.0, f"{display_characters.strip()}\nError")


# Main window for the calculator
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("270x300")
window.resizable(False, False)

# Display for input
entered_characters = tk.Text(window, width=15, height=2, font=("Arial", 24))
entered_characters.grid(row=1, column=1, columnspan=5)

# The characters valid for our calculator,i.e, the button characters
# Note that we want to have 4 columns and 6 rows
characters = (("sin", "cos", "tan", "←"),
              ("7", "8", "9", "+"),
              ("4", "5", "6", "-"),
              ("1", "2", "3", "*"),
              ("(", "0", ")", "/"),
              ("C", ".", "%", "="))

# Creating buttons, note: using range(6) since we want to have 6 rows
# Loop for the rows' section
for i in range(6):

    # Column's section(using range(4) since we want to have 4 columns)
    for j in range(4):
        button = tk.Button(window, width=6, text=characters[i][j], font=("Times New Roman", 14))
        button.grid(row=i + 2, column=j + 1)
    # Note that in the below code we are just changing the command, background and foreground
        if not i:
            button.config(bg="black", fg="white",
                          command=lambda current_character=characters[i][j]: display_text(f"{current_character} ("))
            if j == 3:
                button.config(command=remove_character, bg="red")

        elif i <= 4:
            button.config(bg="gray",
                          command=lambda current_character=characters[i][j]: display_text(current_character))
            button.grid(row=i + 2, column=j + 1)
        else:
            if not j:
                button.config(bg="orange", command=clear_text)
            elif j <= 2:
                button.config(bg="grey",
                              command=lambda current_character=characters[i][j]: display_text(current_character))
                if j == 2:
                    button.config(text="mod%")
            else:
                button.config(bg="green", command=answer)

window.bind("<Return>", lambda event: answer())
window.bind("<BackSpace>", lambda event: remove_character())

window.mainloop()
