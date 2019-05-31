from wikistat import parse

correct = {
    'Stone_Age': [13, 10, 12, 40],
    'Brain': [19, 5, 25, 11],
    'Artificial_intelligence': [8, 19, 13, 198],
    'Python_(programming_language)': [2, 5, 17, 41],
}
start = 'Stone_Age'
end = 'Python_(programming_language)'
path = './wiki/'

count = 0
max_count = len(correct)

result = parse(start, end, path)

for link, params in result.items():
    if link not in correct:
        break
    if params == correct[link]:
        count += 1
    del correct[link]

if count == 0:
    print("Fail!")
elif count == max_count:
    print("Success!")
else:
    print("{}% passed".format(count*100//max_count))

