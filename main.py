from playfair import Playfair
import itertools
import random

# actual_key = 'BEATRIXCDFGHKLMNOPQSUVWYZ'

playfair = Playfair()

def get_formatted_ciphertext(text):
    lines = map(lambda x: x.replace('\n', '').replace(' ', ''), text.readlines())
    padded = map(lambda x: x + 'X' if len(x) % 2 == 1 else x, lines)
    return list(map(lambda x: ' '.join([x[i: i + 2] for i in range(0, len(x), 2)]), padded))


def simulated_annealing(ciphertext):
    parent = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
    random.shuffle(parent)
    playfair.set_key(parent)
    message = playfair.decrypt(ciphertext)

    print(message)



def main():
    with open('./text.txt', 'r') as text:
        ciphertext = ''.join(text.readlines())

        simulated_annealing(ciphertext)

        # for block in decrypted_text:
        #     print(block)


if __name__ == '__main__':
    main()
