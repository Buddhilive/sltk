import re
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# split tokens using white spaces
def whiteSpace(text: str):
    tokens = text.split(' ')
    return tokens

# find emails in a string
def __findEmails(text: str):
    emails = re.findall(r'\S+@\S+\.\S+', text)
    return emails

# find URLs in a string
def __findURLs(text: str):
    urls = re.findall(r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', text)
    return urls

# find decimals in a string
def __findDecimal(text: str):
    decimal = re.findall(r'\d+\.\d+', text)
    return decimal

# find and mask abbreviations in a string
def __maskAbbreviations(text: str):
    abbr = open(f"{ROOT_DIR}/shared/abbr.json", "r")
    abbr = abbr.read()
    abbr = json.loads(abbr)

    for i in abbr:
        replacer = str(i).replace('.', '<dot/> ')
        text = text.replace(i, replacer)
    return text

# find and mask tokens from dictionary
def __fromDictionary(text: str):
    dictionary = open(f"{ROOT_DIR}/shared/dict.json", "r")
    dictionary = dictionary.read()
    dictionary = json.loads(dictionary)
    for i in dictionary:
        replacer = str(i).replace(' ', '<cmb/>')
        text = text.replace(i, replacer)
    
    return text

# find and mask special tokens like emails, URLs, decimal numbers
def __maskSpecial(text: str):
    emails = __findEmails(text)
    urls = __findURLs(text)
    decimals = __findDecimal(text)

    for i in emails:
        replacer = str(i).replace('.', '<dot/>')
        text = text.replace(i, replacer)
    
    for i in urls:
        replacer = str(i).replace('.', '<dot/>')
        text = text.replace(i, replacer)

    for i in decimals:
        replacer = str(i).replace('.', '<dot/>')
        text = text.replace(i, replacer)

    return text


# preprocess and split sentences
def splitSentences(text: str):
    preprocessText = __maskAbbreviations(text)
    preprocessText = __fromDictionary(preprocessText)
    preprocessText = __maskSpecial(preprocessText)
    sentences = re.split(r"\(?[^\.\?\!]+[\.!\?]\)?", preprocessText)
    return sentences