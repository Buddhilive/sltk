import re
import json
import os
from tqdm import tqdm

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# split tokens using white spaces
def whiteSpace(text: str):
    # tokens = text.split(' ')
    tokens = re.split(r"([\s~`!@#$%^&\*\(\){}\[\];:\"'<,\.>\?\/\\\-_+=“”‘’–•])", text)
    finalTokens = list()
    for token in tokens:
        if(token != '' and token != ' '):
            finalTokens.append(token)

    return finalTokens

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

    for i in tqdm(abbr, ascii=True, desc='Masking Abbreviations'):
        replacer = str(i).replace('.', '<dot/> ')
        i = str(i).replace('.', '')
        text = re.sub(r'' + i + r'\.', f'{i}. ', text)
        text = re.sub(r'(^|\.|\s)+(' + i + r'\.)', f' {replacer}', text)
    return text

# find and mask tokens from dictionary
def __fromDictionary(text: str):
    dictionary = open(f"{ROOT_DIR}/shared/dict.json", "r")
    dictionary = dictionary.read()
    dictionary = json.loads(dictionary)
    for i in tqdm(dictionary, ascii=True, desc='Dictionary Lookup'):
        replacer = str(i).replace(' ', '<cmb/>')
        text = text.replace(i, replacer)
    
    return text

# find and mask special tokens like emails, URLs, decimal numbers
def __maskSpecial(text: str):
    emails = __findEmails(text)
    urls = __findURLs(text)
    decimals = __findDecimal(text)

    for i in tqdm(emails, ascii=True, desc='Masking Emails'):
        replacer = str(i).replace('.', '<dot/>')
        text = text.replace(i, replacer)
    
    for i in tqdm(urls, ascii=True, desc='Masking URLs'):
        i = ''.join(i)
        replacer = str(i).replace('.', '<dot/>')
        replacer = replacer.replace('!', '<exc/>')
        replacer = replacer.replace('?', '<que/>')
        text = text.replace(i, replacer)

    for i in tqdm(decimals, ascii=True, desc='Masking decimals'):
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
def normalize(text: str):
    text = text.replace('<dot/>', '.')
    text = text.replace('<exc/>', '!')
    text = text.replace('<que/>', '?')
    text = text.replace('<cmb/>', '')
    text = re.sub(r'(\n|\r)', '', text)
    return text

# check punctuations
def __isPunctuation(char: str):
    punctuations = '[~`!@#$%^&*(){}[];:"\'<,.>?/\\|-_+=“”‘’–•'
    return char in punctuations

# check whitespace
def __isWhitespace(char: str):
    return char == '' or char == ' '

# clean tokens
def __cleanTokens(tokens: list()):
    finalTokens = list()
    for token in tqdm(tokens, ascii=True, desc='Cleaning Tokens'):
        selectedToken = list()
        for char in token:
            if(not __isWhitespace(char) and not __isPunctuation(char)):
                selectedToken.append(char)
        finalTokens.append(''.join(selectedToken))

    return finalTokens

# get default tokens
def __getDefaultTokens():
    dTokens = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", "[NEW]", "[END]"]
    with open(f'{ROOT_DIR}/shared/pre.txt', 'r') as f:
        dTokens.extend(f.read().split('\n'))

    return dTokens

# build vocab
def buildVocab(sentences: list):
    text = ' '.join(sentences)
    text = normalize(text)
    tokens = re.split(r"[\u0000-\u007F]", text.lower())
    tokens = sorted(tokens)

    tokens = __cleanTokens(tokens)

    defaultTokens = __getDefaultTokens()
    defaultLen = len(defaultTokens)
    uniqueTokens = defaultTokens
    for token in tqdm(tokens, ascii=True, desc='Generating Vocab'):
        if(token != '' and token != ' '):
            if(uniqueTokens.count(token) == 0):
                uniqueTokens.append(token)

    print(f'Found {len(uniqueTokens) - defaultLen} unique tokens out of {len(tokens)} tokens.\nTotal {len(uniqueTokens)} Tokens')

    return uniqueTokens

# tokenize
def tokenize(vocab: str, sentences: list):
    tokens = list()
    with open(f'{vocab}', 'r') as f:
        tokens.extend(f.read().split('\n'))
    vectors = list()

    for sentence in tqdm(sentences, ascii=True, desc='Tokenizing'):
        vectors2 = list()
        sentence = normalize(sentence)
        sentence = whiteSpace(sentence)
        vectors2.append(tokens.index('[CLS]'))

        for word in sentence:
            if(tokens.count(word) > 0):
                vectors2.append(tokens.index(word))
            else:
                newWord = list()
                newWord.append(tokens.index('[NEW]'))
                for char in word:
                    if(tokens.count(char) != 0):
                        newWord.append(tokens.index(char))
                    else:
                        newWord.append(tokens.index('[UNK]'))

                newWord.append(tokens.index('[END]'))
                vectors2.extend(newWord)

        vectors2.append(tokens.index('[SEP]'))    
        vectors.append(vectors2)

    return vectors

# decode vectors
def decode(vocab: str, vectors: list):
    tokens = list()
    with open(f'{vocab}', 'r') as f:
        tokens.extend(f.read().split('\n'))

    sentence = list()
    newWord = list()
    isNewWord = False
    isFirst = True
    space = ''
    for vector in vectors:
        if(tokens[vector] == '[NEW]'):
            isNewWord = True
        
        if(tokens[vector] != '[CLS]' and tokens[vector] != '[SEP]'):
            if(isFirst):
                isFirst = False
            elif(not __isPunctuation(tokens[vector])):
                space = ' '
            else:
                space = ''

            if(isNewWord):
                if(tokens[vector] == '[END]'):
                    isNewWord = False
                    sentence.append(f"{space}{''.join(newWord)}")
                    newWord = list()
                else:
                    if(tokens[vector] != '[NEW]'):
                        newWord.append(tokens[vector])

            else:
                sentence.append(f"{space}{tokens[vector]}")
        elif(tokens[vector] == '[SEP]'):
            sentence.append('.')
        
    return ''.join(sentence)

def test(text):
    test = __findURLs(text)
    return test