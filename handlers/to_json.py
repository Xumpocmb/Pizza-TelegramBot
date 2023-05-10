import json

ban_words = []

with open('../ban-words/words.txt', encoding='utf-8') as r:
    for i in r:
        n = i.lower().split('\n')[0]
        if n != '':
            ban_words.append(n)

with open('../ban-words/new-banwords.json', 'w', encoding='utf-8') as e:
    json.dump(ban_words, e)
