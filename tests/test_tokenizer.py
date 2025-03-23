import io
from sltkpy import GPETokenizer

corpus = ''
with io.open('./tests/sample.txt','r',encoding='utf8') as f:
    corpus = f.read()
sample = "ශ්‍රී ලංකාව සිලෝන් ලෙස ද හැඳින් වේ."

def test_tokenizer():
    tokenizer = GPETokenizer()

    tokenizer.train(corpus=corpus, vocab_size=300)
    tokens = tokenizer.tokenize(sample)
    encoded_tokens = tokenizer.encode(tokens)
    decoded_text = tokenizer.decode(encoded_tokens)
    assert decoded_text == sample