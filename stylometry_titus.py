import os

corpus = {
    'Peele': 'corpus/peele',
    'Shakespeare': 'corpus/shakespeare',
    'Disputed': 'corpus/disputed'
}

def read_folder_into_string(path):
    strings = []
    for filename in sorted(os.listdir(path)):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
            strings.append(f.read())
    return '\n'.join(strings)

play_by_author = {}

for author, plays in corpus.items():
    play_by_author[author] = read_folder_into_string(plays)

for author in corpus:
    print(play_by_author[author][:100])