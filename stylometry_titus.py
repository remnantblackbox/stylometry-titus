import os

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

play_by_author = {}

for author, plays in corpus.items():
    play_by_author[author] = read_folder_into_string(plays)

titus_acts = read_folder_into_dict('corpus/disputed')

for author in corpus:
    print(author, '-', play_by_author[author][:100])

for act in titus_acts:
    print(act, '-', titus_acts[act][:100])