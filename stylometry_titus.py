import os
import nltk
import math
nltk.download('punkt_tab')

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

def calculate_feature_freqs(tokens: list[str], features: list[str]) -> dict[str, float]:
    """Calculate each feature's frequency in a token list, as a share of total tokens"""
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

def evaluate_test_case(tokens: list[str], features: list[str], corpus_features: dict[str, dict[str, float]]) -> dict[str, float]:
    """Calculate z-scores for a set of tokens (a test case) against the corpus norm."""
    freqs = calculate_feature_freqs(tokens, features)
    return calculate_zscores(freqs, corpus_features)

def compute_delta(testcase_zscores: dict[str, float], feature_zscores: dict[str, dict[str, float]], features: list[str]) -> dict[str, float]:
    """Compute Burrows' Delta between a test case and each candidate author."""
    deltas = {}
    for author, author_zscores in feature_zscores.items():
        delta = sum(math.fabs(testcase_zscores[feature] - author_zscores[feature]) for feature in features)
        deltas[author] = delta / len(features)
    return deltas

# delta analysis flow to check results with different numbers most frequent words
def run_delta_analysis(n_mfw: int):
    # top-n most frequent words as stylometric features
    features = [word for word, freq in nltk.FreqDist(whole_corpus).most_common(n_mfw)]

    # author's feature frequencies
    feature_freqs = {
        author: calculate_feature_freqs(plays_by_author_tokens[author], features)
        for author in plays_by_author.keys()
    }

    # corpus norm: mean and stdev per feature, across authors
    corpus_features = {}
    num_authors = len(plays_by_author)

    for feature in features:
        corpus_features[feature] = {}

        # mean of means: average each author's frequency for this feature
        feature_average = sum(feature_freqs[author][feature] for author in plays_by_author.keys()) / num_authors
        corpus_features[feature]["Mean"] = feature_average

        # standard deviation (sample formula) across authors
        feature_stdev = sum((feature_freqs[author][feature] - feature_average) ** 2 for author in plays_by_author.keys())
        feature_stdev = math.sqrt(feature_stdev / (num_authors - 1))
        corpus_features[feature]["StdDev"] = feature_stdev

    # authors z-scores
    feature_zscores = {
        author: calculate_zscores(feature_freqs[author], corpus_features)
        for author in plays_by_author.keys()
    }

    # calculate Delta for each titus act
    print(f"\n---- Results with {n_mfw} most frequent words ----")
    for act, tokens in titus_acts_tokens.items():
        act_zscores = evaluate_test_case(tokens, features, corpus_features)
        act_deltas = compute_delta(act_zscores, feature_zscores, features)
        winner = min(act_deltas, key=act_deltas.get)
        print(f"{act}: {winner} ({act_deltas[winner]:.4f}) -- Peele: {act_deltas['Peele']:.4f}, Shakespeare: {act_deltas['Shakespeare']:.4f}")

# robustness check against different top-n most frequent words
for n in (30, 50, 100, 200):
    run_delta_analysis(n)