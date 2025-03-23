import io
import regex
from collections import Counter

class GPETokenizer:
    def __init__(self):
        self.vocab = {}
        self.words = list()

    @staticmethod
    def _get_sinhala_graphemes(text):
        basic_graphemes = regex.findall(r'\X', text)
        
        result = []
        current = ""
        
        for g in basic_graphemes:
            if g.endswith('\u200d'):
                current += g
            elif current:
                current += g
                result.append(current)
                current = ""
            else:
                result.append(g)
        
        if current:
            result.append(current)
            
        return result
    
    def _get_vocab(self, text):
        text = text.replace(" ", "⣿")
        char_to_index = {}
        index = 0
        chars = set(self._get_sinhala_graphemes(text))
        for char in chars:
            if char not in char_to_index:
                char_to_index[char] = index
                index += 1
        return char_to_index
    
    @staticmethod
    def _reverse_dictionary(input_dict):
        return {v: k for k, v in input_dict.items()}
    
    def _get_frequency(self):
        freq_map = Counter()
        for word in self.words:
            freq_map["⣹".join(self._get_sinhala_graphemes(word)) + "⣹⣿"] += 1
        return freq_map
    
    @staticmethod
    def _get_pairs(freq_map, minimum_freq = 1):
        pairs = Counter()
        for word, freq in freq_map.items():
            if freq < minimum_freq:
                break
            symbols = word.split('⣹')
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs
    
    def _merge_pairs(self, pairs, freq_map):
        new_freq_map = {}
        best_pair = max(pairs, key=pairs.get)
        bigram = regex.escape("⣹".join(best_pair))
        pattern = regex.compile(bigram)
        new_vocab = "".join(best_pair)
        for word in freq_map:
            new_word = pattern.sub(new_vocab, word)
            new_freq_map[new_word] = freq_map[word]
        self.vocab[new_vocab] = len(self.vocab)
        return new_freq_map
    
    @staticmethod
    def _flatten(list_of_lists):
        return [item for sublist in list_of_lists for item in sublist]
    
    def train(self, corpus, vocab_size = 30, min_freq = 3):
        self.vocab = self._get_vocab(corpus)
        self.words = corpus.split()
        freq_map = self._get_frequency()
        while len(self.vocab) < vocab_size:
            pairs = self._get_pairs(freq_map, min_freq)
            if not pairs:
                break
            freq_map = self._merge_pairs(pairs, freq_map)
        return self.vocab
    
    def load_vocab(self, vocab):
        self.vocab = vocab

    def tokenize(self, text):
        tokens = []
        words = text.split()
        for word in words:
            word = "⣹".join(self._get_sinhala_graphemes(word)) + "⣹⣿"
            for subword in self.vocab:
                word = word.replace("⣹".join(self._get_sinhala_graphemes(subword)), subword)
            tokens.append(word.split("⣹"))
        return self._flatten(tokens)
    
    def encode(self, tokens):
        encoded_tokens = []
        for token in tokens:
            enc_tok = self.vocab[token]
            encoded_tokens.append(enc_tok)
        return encoded_tokens
    
    def decode(self, encoded_tokens):
        decoded_text = ""
        rev_vocab = self._reverse_dictionary(self.vocab)
        for enc_tok in encoded_tokens:
            subword = rev_vocab[enc_tok]
            decoded_text += subword.replace('⣿', ' ')
        return decoded_text.rstrip()
