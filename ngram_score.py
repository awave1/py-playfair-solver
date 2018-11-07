from math import log10

class NgramScore:
    def __init__(self, ngram_file, sep=''):
        self.ngrams = {}

        with open(ngram_file) as file:
            for line in file.readlines():
                key, count = file.readline().split(sep)
                self.ngrams[key] = int(count)

            self.L = len(key)