from math import log10


class QGramScore:
    def __init__(self, qgram_file):
        self.ngrams = {}
        self.key_len = 4

        with open(qgram_file) as file:
            for line in file.readlines():
                key, count = line.split(' ')
                self.ngrams[key] = int(count)

        self.N = sum(self.ngrams.values())

        # calculate log probabilities
        for key in self.ngrams.keys():
            self.ngrams[key] = log10(float(self.ngrams[key]) / self.N)

        # In order to floor all probabilities
        self.floor = log10(0.01 / self.N)

    def score(self, text):
        """
        Compute the score of provided text using qgram
        :param text:
        :return:
        """

        score = 0

        for i in range(len(text) - self.key_len + 1):

            # get every 4 letters of the string
            key = text[i: i + self.key_len]

            if key in self.ngrams:
                score += self.ngrams[key]
            else:
                score += self.floor

        return score
