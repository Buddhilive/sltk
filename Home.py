import io
import streamlit as st
from sltkpy import sltk

corpus = ''
with io.open('data/sample.txt','r',encoding='utf-8', errors='replace') as f:
    corpus = f.read()

sentences = sltk.splitSentences(corpus)
tokens = sltk.buildVocab(sentences)

st.write(tokens)