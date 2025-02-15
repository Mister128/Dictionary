import flet as ft
import json
import os

show_words_color = "purple"
add_word_color = "green"
dictionary = "Dictionary.docx"
theme = "dark"

colors = {
    "purple": "purple",
    "green": "green",
    "lightgreen": "lightgreen",
    "lime": "lime",
    "red": "red",
    "indigo": "indigo",
    "blue": "blue",
    "cyan": "cyan",
    "teal": "teal",
    "pink": "pink",
    "yellow": "yellow",
    "amber": "amber",
    "orange": "orange",
}

def files_list(directory):
    all_files = os.listdir(directory)
    docx_files = [file for file in all_files if file.endswith('.docx')]
    return docx_files

def push_changes_to_json():
    os.remove("preset.json")

    with open("preset.json", "w") as f:
        to_json = {"show_words_color": show_words_color,
                   "add_word_color": add_word_color,
                   "dictionary": dictionary,
                   "theme": theme}
        json.dump(to_json, f)
        
def delete_file(filename):
    try:
        os.remove(os.path.join('./dictionaries', filename))
    except Exception as e:
        print(f"Error deleting file: {e}")


def rename_file(old_filename, new_filename):
    try:
        os.rename(os.path.join('./dictionaries', old_filename), os.path.join('./dictionaries', new_filename + '.docx'))
    except Exception as e:
        print(f"Error renaming file: {e}")