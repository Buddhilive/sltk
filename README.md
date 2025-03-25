# SLTK: A Comprehensive Tokenizer for Sinhala Language

Welcome to the GitHub repository for SLTK, a powerful tokenizer designed to enhance Sinhala Natural Language Processing (NLP) tasks. SLTK implements Grapheme Pair Encoding for tokenizing. Although our first [SLTK version](https://github.com/Buddhilive/sltk/tree/legacy) was implemented using [our own research](http://dx.doi.org/10.13140/RG.2.2.21084.40322), this is implemented inspired by the research paper by [Velayuthan et al. (2024).](https://arxiv.org/abs/2409.11501)

## Installation

To install SLTK, run following command:
```shell
pip install sltkpy
```

## Usage

You can train the tokenizer on a custom dataset to create your own vabulary and use it to tokenize your text data. First, import SLTK:
```py
from sltkpy import GPETokenizer
```
Now initialize the tokenizer:
```py
tokenizer = GPETokenizer()
```

### Train new vocab
To train a new vocab, provide `corpus` to the `train` method. Additionally you can provide the maximum size of vocab to `vocab_size` and the minimum frequency for a pair to be qualified as a vocab by setting `min_freq`.
```py
vocab = tokenizer.train(corpus=corpus, vocab_size=3000)
```
> Note: Default value of `min_freq` is 3.

Once the training is finished, the method will return the vocab as a dictionary. You can save it as a JSON file to use it in future.

### Load vocab
There are two ways to load vocab to the tokenizer. Either you can use your own vocab or you can load the pre-trained vocab available within the SLTK library. It is trained on [Wikipedia Sinhala Dataset on Huggingface Datasets](https://huggingface.co/datasets/wikimedia/wikipedia/viewer/20231101.si).

1. Load pre-trained vocab:
```py
tokenizer.pre_load()
```
2. Load your own trained vocab:
```py
tokenizer.load_vocab('<path_to_your_vocab>.json')
```
### Tokenize text
Once you have loaded vocab using any method above, you can tokenize your text as follows:
```py
tokens = tokenizer.tokenize('ශ්‍රී ලංකාව සිලෝන් ලෙස ද හැඳින් වේ.')
```

### Encode tokens
To encode tokens, use following method:
```py
encoded_tokens = tokenizer.encode(tokens)
```

### Decode tokens
To decode tokens, use the following method:
```py
decoded_text = tokenizer.decode(encoded_tokens)
```