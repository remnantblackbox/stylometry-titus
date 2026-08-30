import os
import nltk
import math

corpus = {
    'Peele': 'corpus/peele',
    'Shakespeare': 'corpus/shakespeare'
}

def read_folder_into_string(path):
    strings = []
    for filename in sorted(os.listdir(path)):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            strings.append(f.read())
    return '\n'.join(strings)

def read_folder_into_dict(path):
    texts = {}
    for filename in sorted(os.listdir(path)):
        name = os.path.splitext(filename)[0]
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            texts[name] = f.read()
    return texts

plays_by_author = {}

for author, plays in corpus.items():
    plays_by_author[author] = read_folder_into_string(plays)

titus_acts = read_folder_into_dict('corpus/disputed')

def tokenize_corpus(texts):
    tokenized = {}
    for name, text in texts.items():
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if any(c.isalpha() for c in token)]
        tokens = [tok.lower() for tok in tokens]
        tokenized[name] = tokens
    return tokenized

plays_by_author_tokens = tokenize_corpus(plays_by_author)
titus_acts_tokens = tokenize_corpus(titus_acts)