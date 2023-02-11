import re
import json
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# split tokens using white spaces
def whiteSpace(text: str):
    tokens = text.split(' ')

    uniqueTokens = list()
    for token in tokens:
        if(token != '' and token != ' '):
            if(uniqueTokens.count(token) == 0):
                uniqueTokens.append(token)

    return tokens

# find emails in a string
def __findEmails(text: str):
    emails = re.findall(r'\S+@\S+\.\S+', text)
    return emails

# find URLs in a string
def __findURLs(text: str):
    urls = re.findall(r'((?:http|ftp|https):\/\/)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', text)
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
        i = str(i).replace('.', '')
        text = re.sub(r'(^|\.|\s|)+(' + i + r'\.)', f' {replacer}', text)
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
        i = ''.join(i)
        replacer = str(i).replace('.', '<dot/>')
        replacer = replacer.replace('!', '<exc/>')
        replacer = replacer.replace('?', '<que/>')
        text = text.replace(i, replacer)

    for i in decimals:
        replacer = str(i).replace('.', '<dot/>')
        text = text.replace(i, replacer)

    return text

# preprocess and split sentences
def splitSentences(text: str):
    preprocessText = re.sub(r'\.(?=\S\W)', '. ', text)
    # print(preprocessText)
    preprocessText = __maskAbbreviations(preprocessText)
    preprocessText = __fromDictionary(preprocessText)
    preprocessText = __maskSpecial(preprocessText)
    sentences = re.split(r"[.!?]", preprocessText)
    return sentences

# normalize masked text
def __normalize(text: str):
    text = text.replace('<dot/>', '.')
    text = text.replace('<exc/>', '!')
    text = text.replace('<que/>', '?')
    text = text.replace('<cmb/>', '')
    text = re.sub(r'(\n|\r)', '', text)
    return text

# sunword tokenize
def __subwordTokenizer(tokens: list):
    newTokens = tokens
    tokenList = list()

    for token in tokens:
        charIndex = 1
        charToken = token
        charCount = 0

        for subword in tokenList:
            token = token.replace(subword, '')

        for newToken in token:
            if(len(token) > charIndex):
                charIndex = charIndex + 1
                charToken = ''.join(token[:charIndex])

                for word in tokens:
                    if(charToken in word):
                        charCount = charCount + 1
            
        if(charCount > 0):
            tokenList.append(charToken)

    return tokenList

# tokenize
def tokenize(sentences: list):
    text = ' '.join(sentences)
    text = __normalize(text)
    tokens = re.split(r"[\u0000-\u007F]", text)
    tokens = sorted(tokens)

    """ uniqueTokens = dict()
    for token in tokens:
        if(token != '' and token != ' '):
            if(token in uniqueTokens.keys()):
                uniqueTokens[token] = uniqueTokens[token] + 1
            else:
                uniqueTokens[token] = 1 """

    uniqueTokens = list()
    for token in tokens:
        if(token != '' and token != ' '):
            if(uniqueTokens.count(token) == 0):
                uniqueTokens.append(token)

    print(f'Found {len(uniqueTokens)} unique tokens out of {len(tokens)} tokens')

    return uniqueTokens

def test(text):
    test = __findURLs(text)
    return test