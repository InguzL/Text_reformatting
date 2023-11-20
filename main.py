from tkinter import *
from tkinter.scrolledtext import ScrolledText
import pyperclip
import re
pattern = r'[^\w0-9\., \'?!-]'


#  Picks the conversion type based on what the user has selected
def generate_text():

    source_text = text_input.get("1.0", END)
    conversion_type = variable.get()
    clean_text = text_cleanup(source_text)

    if conversion_type == "Synopsis":
        converted_string = convert_synopsis(clean_text)
    elif conversion_type == "Cast":
        converted_string = convert_cast(clean_text)
    elif conversion_type == "Other":
        converted_string = clean_text

    on_rerun_button()
    text_output.insert(1.0, chars=converted_string)
    pyperclip.copy(converted_string)


#  Converts synopses in such a way that it removes all excess spaces, adds a capital letter at the start and makes
#  sure there's a full stop at the end
def convert_synopsis(source):
    converted_string = ""
    string_list = source.split(" ")
    new_string_list = [string.strip() for string in string_list if string != ""]
    #  print(new_string_list)
    for item in new_string_list:
        if " " not in item:
            if item in new_string_list[0]:
                item.title()
            converted_string += item
            if item in new_string_list[:-1]:
                converted_string += " "

    return converted_string


#  Converts cast lists in such a way that it removes all excess spaces and capitalises all names
def convert_cast(source):
    converted_string = ""
    # print(source)
    string_list = source.split(",")
    # print(f"old string list: {string_list}")
    new_string_list = [string.strip().title() for string in string_list if string != ""]
    # print(f"New string list: {new_string_list}")
    for item in new_string_list:
        if "," not in item:

            converted_string += item
            if item in new_string_list[:-1]:
                converted_string += ", "

    return converted_string


#  Cleans up text so that all line jumps are replace by a space, removes any excess characters, encodes then decodes
#  text to ensure everything is consistent and finally joins everything back into one string
def text_cleanup(source):
    # print(source)
    no_line_jumps = source.replace("\n", " ").replace('\r', '')
    # print(no_line_jumps)
    clean_text = re.sub(pattern, '', no_line_jumps)
    # print(clean_text)
    source_encode = clean_text.encode(encoding="ascii", errors="ignore")
    source_decode = source_encode.decode()
    decoded_text = " ".join([word for word in source_decode.split()])

    return decoded_text


#  Removes any text in the output box before re-running a conversion job
def on_rerun_button():
    text_output.configure(state='normal')
    text_output.delete('1.0', END)


window = Tk()
window.title("Text conversion")
window.config(padx=50, pady=50)

text_input = ScrolledText(width=150, height=10)
text_input.grid(row=0, column=0, columnspan=2)

variable = StringVar(window)
variable.set("Synopsis")  # default value
format_options = OptionMenu(window, variable, "Synopsis", "Cast", "Other")
format_options.grid(row=1, column=0)

generate_output = Button(text="Convert", highlightthickness=0, command=generate_text)
generate_output.grid(row=1, column=1)

text_output = ScrolledText(width=150, height=10)
text_output.grid(row=3, column=0, columnspan=3)


window.mainloop()

