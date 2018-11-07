import re


def prepare_message(message):
    return re.sub(r'[^A-Z]', '', message.upper())


class Playfair:
    def __init__(self, key='ABCDEFGHIKLMNOPQRSTUVWXYZ'):
        self.key = [k.upper() for k in key]

    def set_key(self, key):
        self.key = key

    def encrypt(self, message, format=False, block_len=2, as_list=False):
        encrypted_message = ''
        message = prepare_message(message)
        message = re.sub(r'[J]', 'I', message)

        # Pad message with 'X' if it's odd length
        if len(message) % 2 == 1:
            message += 'X'

        for m in range(0, len(message), 2):
            a = message[m]
            b = message[m + 1]

            encrypted_message += self.__encrypt_pair(a, b)

        if format:
            encrypted_message = ' '.join(
                [encrypted_message[i: i + block_len] for i in range(0, len(encrypted_message), block_len)]
            )

        return encrypted_message if not as_list else encrypted_message.split(' ')

    def __encrypt_pair(self, a, b):
        if a == b:
            b = 'X'

        a_row, a_col = int(self.key.index(a) / 5), self.key.index(a) % 5
        b_row, b_col = int(self.key.index(b) / 5), self.key.index(b) % 5

        if a_row == b_row:
            return self.key[a_row * 5 + (a_col + 1) % 5] + self.key[b_row * 5 + (b_col + 1) % 5]
        elif a_col == b_col:
            return self.key[((a_row + 1) % 5) * 5 + a_col] + self.key[((b_row + 1) % 5) * 5 + b_col]
        else:
            return self.key[a_row * 5 + b_col] + self.key[b_row * 5 + a_col]

    def decrypt(self, ciphertext, format=False, block_len=2, as_list=False):
        message = ''
        ciphertext = prepare_message(ciphertext)

        if len(ciphertext) % 2 == 1:
            ciphertext += 'X'

        for c in range(0, len(ciphertext), 2):
            a = ciphertext[c]
            b = ciphertext[c + 1]

            message += self.__decrypt_pair(a, b)

        if format:
            message = ' '.join([message[i: i + block_len] for i in range(0, len(message), block_len)])

        return message if not as_list else message.split(' ')

    def __decrypt_pair(self, a, b):
        a_row, a_col = int(self.key.index(a) / 5), self.key.index(a) % 5
        b_row, b_col = int(self.key.index(b) / 5), self.key.index(b) % 5

        if a_row == b_row:
            return self.key[a_row * 5 + (a_col - 1) % 5] + self.key[b_row * 5 + (b_col - 1) % 5]
        elif a_col == b_col:
            return self.key[((a_row - 1) % 5) * 5 + a_col] + self.key[((b_row - 1) % 5) * 5 + b_col]
        else:
            return self.key[a_row * 5 + b_col] + self.key[b_row * 5 + a_col]