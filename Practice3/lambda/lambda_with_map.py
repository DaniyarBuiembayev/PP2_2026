words = ["cat", "elephant", "dog", "tiger"]

long_words = list(filter(lambda w: len(w) > 4, words))

print(long_words)
