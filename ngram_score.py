from math import log10


class NGramScore:
    def __init__(self, ngram_file):
        self.ngrams = {}

        key = ''

        with open(ngram_file) as file:
            for line in file.readlines():
                key, count = line.split(' ')
                self.ngrams[key] = int(count)

            self.L = len(key)
            self.N = sum(self.ngrams.values())

            # calculate log probabilities
            for key in self.ngrams.keys():
                self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)

            # In order to floor all probabilities
            self.floor = log10(0.01 / self.N)

    def score(self, text):
        score = 0

        for i in range(len(text) - self.L + 1):
            key = text[i: i + self.L]

            if key in self.ngrams:
                score += self.ngrams[key]
            else:
                score += self.floor

        return score
