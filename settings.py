import json
import os
show_words_color = "purple"
add_word_color = "green"

def push_changes_to_json():
    os.remove("preset.json")

    with open("preset.json", "w") as f:
        to_json = {"show_words_color": show_words_color,
                   "add_word_color": add_word_color}
        json.dump(to_json, f)