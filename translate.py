import json


languages = {
    "en": "English",
    "ru": "Русский"
}
language = "en"

messages = {}

for lang in languages.keys():
    with open(file="localization/" + lang + "/messages.json",
              mode="r",
              encoding="utf-8") as jsonFile:
        messages[lang] = json.load(jsonFile)


def changeLanguage():
    global language
    ls = list(languages.keys())
    li = ls.index(language)
    if -1 < li < len(ls) - 1:
        language = ls[li + 1]
    else:
        language = ls[0]


def t(text, *args):
    if text in messages[language].keys():
        formatted_text = messages[language][text].format(*args)
        return formatted_text
    else:
        return text
