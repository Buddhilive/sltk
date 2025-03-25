import io
import json
import regex
from collections import Counter

class GPETokenizer:
    def __init__(self):
        """
        Initialize the GPETokenizer object.

        The GPETokenizer object doesn't require any parameters to be initialized.
        The vocab and words attributes are initialized as empty dictionaries and
        lists respectively.
        """
        self.vocab = {}
        self.words = list()

    @staticmethod
    def _get_sinhala_graphemes(text):
        """
        Gets the Sinhala graphemes from a given text.

        This function takes a given text and returns a list of Sinhala graphemes.
        It uses the regex library to find all the graphemes in the text and
        then processes these graphemes to create a list of Sinhala graphemes.

        Args:
            text (str): The text from which to extract the graphemes.

        Returns:
            list: A list of Sinhala graphemes extracted from the text.
        """
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
        """
        Generates a vocabulary dictionary from the given text.

        This function takes a given text, extracts all the unique Sinhala
        graphemes from it, and creates a dictionary where the keys are the
        graphemes and the values are the indices.

        Args:
            text (str): The text from which to generate the vocabulary.

        Returns:
            dict: A dictionary where the keys are the graphemes and the values
            are the indices.
        """
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
        """
        Reverses a given dictionary.
        
        This function takes a given dictionary and returns a new dictionary
        where the keys and values are swapped.
        
        Args:
            input_dict (dict): The dictionary to reverse.
        
        Returns:
            dict: A reversed dictionary.
        """
        return {v: k for k, v in input_dict.items()}
    
    def _get_frequency(self):
        """
        Calculates the frequency of each word in the given text.

        This function takes the given words and calculates the frequency of
        each word. It returns a Counter object where the keys are the words
        and the values are the frequencies.

        Returns:
            collections.Counter: A Counter object where the keys are the words
            and the values are the frequencies.
        """
        freq_map = Counter()
        for word in self.words:
            freq_map["⣹".join(self._get_sinhala_graphemes(word)) + "⣹⣿"] += 1
        return freq_map
    
    @staticmethod
    def _get_pairs(freq_map, minimum_freq = 1):
        """
        Get pairs of symbols from the given frequency map.

        This function takes a given frequency map and returns a Counter object
        where the keys are pairs of symbols and the values are the frequencies of
        these pairs.

        Args:
            freq_map (collections.Counter): A Counter object where the keys are
                the words and the values are the frequencies.

            minimum_freq (int): The minimum frequency a pair must have to be
                included in the result.

        Returns:
            collections.Counter: A Counter object where the keys are pairs of
                symbols and the values are the frequencies of these pairs.
        """
        pairs = Counter()
        for word, freq in freq_map.items():
            if freq < minimum_freq:
                break
            symbols = word.split('⣹')
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs
    
    def _merge_pairs(self, pairs, freq_map):
        """
        Merge the most common pair of symbols in the given frequency map.

        This function takes a given frequency map and merges the most common
        pair of symbols into a new symbol. The new symbol is added to the
        vocabulary and the frequency map is updated accordingly.

        Args:
            pairs (collections.Counter): A Counter object where the keys are
                pairs of symbols and the values are the frequencies of these
                pairs.

            freq_map (collections.Counter): A Counter object where the keys are
                the words and the values are the frequencies.

        Returns:
            collections.Counter: The updated frequency map.
        """
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
        """
        Flattens a list of lists into a single list.

        This function takes a list of lists and returns a single list that
        contains all the elements of the original lists.

        Args:
            list_of_lists (list): A list of lists

        Returns:
            list: A single list containing all the elements of the original
            lists.
        """
        return [item for sublist in list_of_lists for item in sublist]
    
    def train(self, corpus, vocab_size = 30, min_freq = 3):
        """
        Trains the tokenizer to generate a vocabulary of a given size from a
        given corpus.

        This function takes a given corpus and a desired vocabulary size and
        generates a vocabulary of that size from the corpus. The vocabulary is
        generated by merging the most common pair of symbols in the corpus
        repeatedly until the desired vocabulary size is reached.

        Args:
            corpus (str): The corpus from which to generate the vocabulary.

            vocab_size (int): The desired size of the vocabulary. Defaults to
                30.

            min_freq (int): The minimum frequency of a pair of symbols to be
                considered for merging. Defaults to 3.

        Returns:
            dict: The generated vocabulary
        """
        self.vocab = self._get_vocab(corpus)
        self.words = corpus.split()
        freq_map = self._get_frequency()
        while len(self.vocab) < vocab_size:
            pairs = self._get_pairs(freq_map, min_freq)
            if not pairs:
                break
            freq_map = self._merge_pairs(pairs, freq_map)
        return self.vocab
    
    def load_vocab(self, file_path):
        try:
            with io.open(file_path, 'r', encoding='utf-8') as f:
                json_content = f.read()
                self.vocab = json.loads(json_content)
        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON format in {file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def tokenize(self, text):
        """
        Tokenizes the given text into subwords using the learned vocabulary.

        This function takes a given text and tokenizes it into subwords using
        the learned vocabulary. The tokenization is done by splitting the text
        into words, splitting each word into graphemes, and then replacing each
        grapheme with its corresponding subword from the vocabulary. The
        resulting list of subwords is then flattened into a single list.

        Args:
            text (str): The text to tokenize.

        Returns:
            list: A list of subwords.
        """

        tokens = []
        words = text.split()
        for word in words:
            word = "⣹".join(self._get_sinhala_graphemes(word)) + "⣹⣿"
            for subword in self.vocab:
                word = word.replace("⣹".join(self._get_sinhala_graphemes(subword)), subword)
            tokens.append(word.split("⣹"))
        return self._flatten(tokens)
    
    def encode(self, tokens):
        """
        Encodes the given list of tokens into a list of integers using the vocabulary.

        This function takes a list of tokens and returns a list of integers where
        each integer corresponds to the index of the token in the vocabulary.

        Args:
            tokens (list): A list of tokens to encode.

        Returns:
            list: A list of integers representing the encoded tokens.
        """
        encoded_tokens = []
        for token in tokens:
            enc_tok = self.vocab[token]
            encoded_tokens.append(enc_tok)
        return encoded_tokens
    
    def decode(self, encoded_tokens):
        """
        Decodes a list of encoded tokens back into a string.

        This function takes a list of integers (encoded tokens) and decodes them
        using the reverse vocabulary mapping to reconstruct the original text.
        The decoding process involves replacing special characters with spaces
        and concatenating the subwords to form the final decoded text.

        Args:
            encoded_tokens (list): A list of integers representing the encoded tokens.

        Returns:
            str: The decoded text as a string.
        """

        decoded_text = ""
        rev_vocab = self._reverse_dictionary(self.vocab)
        for enc_tok in encoded_tokens:
            subword = rev_vocab[enc_tok]
            decoded_text += subword.replace('⣿', ' ')
        return decoded_text.rstrip()
