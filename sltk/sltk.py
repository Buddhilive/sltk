import re

def whiteSpace(text):
    tokens = text.split(' ')
    return tokens

def splitSentences(text):
    sentences = re.findall(r"\(?[^\.\?\!]+[\.!\?]\)?", text)
    return sentences

def __findEmails(text):
    emails = re.findall(r'\S+@\S+\.\S+', text)
    return emails