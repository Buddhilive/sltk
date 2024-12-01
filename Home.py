import io
import streamlit as st
from sltkpy import sltk
import numpy as np
import pandas as pd

st.title("SLTK: Sinhala Language Toolkit")
st.write("SLTK, a powerful tokenizer designed to enhance Sinhala Natural Language Processing (NLP) tasks.")

corpus = ''
with io.open('data/sample.txt','r',encoding='utf-8', errors='replace') as f:
    corpus = f.read()

# split sentences
sentences = sltk.splitSentences(corpus)

# generate tokens
tokens = sltk.buildVocab(sentences)

# Convert to DataFrame
df = pd.DataFrame(np.array(tokens), columns=["Tokens"])

# Display as a static table
st.header("Tokens")
st.dataframe(df, width=300)

# save vocab
sltk.save(tokens, 'models/vocab.txt')

# initialize tokenizer from the vocab
tokenizer = sltk.Tokenizer('models/vocab.txt')

# generate vectors
vectors = tokenizer.tokenize(sentences)

# max length of a vector
st.header("Test tokenizer")
st.text_input("Max length of a vector", len(max(vectors, key=len)), disabled=True)

# test tokenizer
st.text_area("Vector", vectors[2], disabled=True)
st.text_area("Decoded vector", tokenizer.decode(vectors[2]), disabled=True)