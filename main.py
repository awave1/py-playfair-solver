from playfair import Playfair
from ngram_score import QGramScore
import math
import random
import sys

# actual_key = 'BEATRIXCDFGHKLMNOPQSUVWYZ'

playfair = Playfair()
qgram = QGramScore('english_quadgrams.txt')

TEMP = 20
STEP = 0.2
COUNT = 100
DEFAULT_KEY = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'


def get_formatted_ciphertext(text):
    lines = map(lambda x: x.replace('\n', '').replace(' ', ''), text.readlines())
    padded = map(lambda x: x + 'X' if len(x) % 2 == 1 else x, lines)
    return list(map(lambda x: ' '.join([x[i: i + 2] for i in range(0, len(x), 2)]), padded))


# 1. Generate a random key, called the 'parent', decipher the ciphertext
#     using this key.
# 2. Rate the fitness of the deciphered text, store the result.
# 3. for(TEMP = 10;TEMP >= 0; TEMP = TEMP - STEP)
#       for (count = 50,000; count>0; count--)
#          Change the parent key slightly (e.g. swap two characters in the
#            key at random) to get child key,
#          Measure the fitness of the deciphered text using the child key
#          set dF = (fitness of child - fitness of parent)
#          If dF > 0 (fitness of child is higher than parent key),
#              set parent = child
#          If dF < 0 (fitness of child is worse than parent),
#              set parent = child with probability e^(dF/T).


def swap_random(l):
    i = range(len(l))
    a, b = random.sample(i, 2)
    l[a], l[b] = l[b], l[a]


def swap_rand_cols(matrix):
    a, b = random.sample(range(5), 2)
    for col in matrix:
        col[a], col[b] = col[b], col[a]


def key_to_matrix(key):
    return list(map(lambda x: list(x), [key[i: i + 5] for i in range(0, 25, 5)]))


def matrix_to_key(matrix):
    return ''.join(list(map(lambda x: ''.join(x), matrix)))


def modify_key(key):
    matrix_key = key_to_matrix(key)

    operation = random.randint(0, 10)

    if operation == 1: # swap random rows
        swap_random(matrix_key)
        result = matrix_to_key(matrix_key)
    elif operation == 2:
        swap_rand_cols(matrix_key)
        result = matrix_to_key(matrix_key)
    elif operation == 3: # reverse key
        result = matrix_to_key(matrix_key[::-1])
    else:
        key_copy = list(key)
        swap_random(key_copy)
        result = ''.join(key_copy)

    return result


def simulated_annealing(ciphertext):
    parent = list(DEFAULT_KEY)
    random.shuffle(parent)
    parent = ''.join(parent)
    playfair.set_key(parent)

    message = playfair.decrypt(ciphertext)

    best_score = qgram.score(message)
    max_score = best_score

    t = 10
    step = 2

    while t >= 0:
        for count in range(0, COUNT, 1):
            child = modify_key(parent)
            playfair.set_key(child)

            message = playfair.decrypt(ciphertext)
            child_score = qgram.score(message)

            d_f = child_score - max_score

            if d_f > 0:
                max_score = child_score
                parent = child
            elif t > 0:
                probability = math.exp(d_f / t)

                if probability > (1.0 * random.getrandbits(1)):
                    max_score = child_score
                    parent = child

            if max_score > best_score:
                best_score = max_score

        t -= step

    return best_score, parent


def main():
    with open('./text.txt', 'r') as text:
        ciphertext = ''.join(text.readlines())

        i = 0
        max_score = float('-inf')
        while True:
            i += 1

            score, key = simulated_annealing(ciphertext)

            if score > max_score:
                max_score = score
                playfair.set_key(key)

                print(f'best score {max_score}')
                print(f'key: {key}')
                print(f'message: {playfair.decrypt(ciphertext)}')


if __name__ == '__main__':
    main()
