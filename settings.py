import flet as ft
import json
import os
import shutil
import subprocess

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

def files_list():
    all_files = os.listdir("./dictionaries")
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

def import_docx(paths):
    if not paths:
        return
    for path in paths:
        shutil.copy(path, f"./dictionaries/{os.path.basename(path)}")

def export_docx(paths):
    if os.name == 'posix':  # Linux/macOS
        downloads_folder = os.path.expanduser('~/Downloads')
    elif os.name == 'nt':  # Windows
        downloads_folder = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        raise OSError("Не удалось определить операционную систему.")
    for path in paths:
        filename = os.path.basename(path)  # Получаем имя файла
        full_path = os.path.join(downloads_folder, filename)  
        shutil.copy(path, full_path)
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['explorer', downloads_folder])
        elif os.name == 'posix':  # Unix-like systems (macOS, Linux)
            if 'Darwin' in platform.platform():  # For macOS
                subprocess.Popen(['open', downloads_folder])
            else:  # For Linux
                subprocess.Popen(['xdg-open', downloads_folder])
    except Exception as e:
        print(f"Ошибка при открытии папки: {e}")
    