import os
import nltk
import math

authors_folder = {
    'Peele': 'corpus/peele',
    'Shakespeare': 'corpus/shakespeare'
}

titus_folder = 'corpus/disputed'

def read_folder_texts(path: str) -> dict[str, str]:
    """Read every file in a folder and return a dict {filename: text}"""
    texts = {}
    for filename in sorted(os.listdir(path)):
        name = os.path.splitext(filename)[0]
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            texts[name] = f.read()
    return texts

def tokenize_corpus(texts: dict[str, str]) -> dict[str, list[str]]:
    """Tokenize and clean each text in a corpus."""
    tokenized = {}
    for name, text in texts.items():
        tokens = nltk.word_tokenize(text)
        tokens = [token.lower() for token in tokens if any(c.isalpha() for c in token)]
        tokenized[name] = tokens
    return tokenized

# merge each author's play in a single string because distinction by play is not needed
plays_by_author = {author: '\n'.join(read_folder_texts(path).values()) for author, path in authors_folder.items()}

# keeping titus act separated to test each act individually against each author's corpus
titus_acts = read_folder_texts(titus_folder)

plays_by_author_tokens = tokenize_corpus(plays_by_author)
titus_acts_tokens = tokenize_corpus(titus_acts)

# building a whole corpus (authors only) to get the 30 most frequent words
whole_corpus = []
for author in plays_by_author.keys():
    whole_corpus += plays_by_author_tokens[author]

whole_corpus_freq_dist = list(nltk.FreqDist(whole_corpus).most_common(30))
features = [word for word, freq in whole_corpus_freq_dist]

def calculate_feature_freqs(tokens: list[str], features: list[str]) -> dict[str, float]:
    """Compute each feature's frequency in a token list, as a share of total tokens"""
    overall = len(tokens)
    return {feature: tokens.count(feature) / overall for feature in features}


def calculate_zscores(freqs: dict[str, float], corpus_features: dict[str, dict[str, float]]) -> dict[str, float]:
    """Convert feature frequencies into z-scores relative to the corpus norm"""
    zscores = {}
    for feature, freq in freqs.items():
        mean = corpus_features[feature]["Mean"]
        stdev = corpus_features[feature]["StdDev"]
        zscores[feature] = (freq - mean) / stdev
    return zscores