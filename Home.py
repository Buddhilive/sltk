import io
import streamlit as st
from sltkpy import sltk

corpus = ''
with io.open('data/sample.txt','r',encoding='utf-8', errors='replace') as f:
    corpus = f.read()

sentences = sltk.splitSentences(corpus)
tokens = sltk.buildVocab(sentences)

st.write(tokens)

sltk.save(tokens, 'models/vocab.txt')
tokenizer = sltk.Tokenizer('models/vocab.txt')

vectors = tokenizer.tokenize(sentences)
st.write(len(max(vectors, key=len)))
st.write(tokenizer.decode(vectors[2]))