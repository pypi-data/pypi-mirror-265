class PlayfairCipher:

    def __init__(self, key_str: str):
        super().__init__()
        self._key_str = self._prepare_key(key_str)
        self._matrix = self._generate_matrix()

    @property
    def key_str(self) -> str:
        return self._key_str

    @key_str.setter
    def key_str(self, key_str: str) -> None:
        self._key_str = self._prepare_key(key_str)
        self._matrix = self._generate_matrix()

    @property
    def matrix(self):
        return self._matrix

    def _prepare_key(self, key_str: str) -> str:
        unique_chars = []
        for char in key_str.lower().replace("j", "i"):
            if char not in unique_chars:
                unique_chars.append(char)
        for char in "abcdefghiklmnopqrstuvwxyz":
            if char not in unique_chars:
                unique_chars.append(char)
        return "".join(unique_chars)

    def _generate_matrix(self):
        matrix = [['' for _ in range(5)] for _ in range(5)]
        k = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = self._key_str[k]
                k += 1
        return matrix

    def _get_coordinates(self, char: chr):
        for i, row in enumerate(self._matrix):
            if char in row:
                return i, row.index(char)
        return -1, -1

    def _encrypt_pair(self, pair):
        row1, col1 = self._get_coordinates(pair[0])
        row2, col2 = self._get_coordinates(pair[1])
        if row1 == row2:
            return self._matrix[row1][(col1 + 1) % 5] + self._matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            return self._matrix[(row1 + 1) % 5][col1] + self._matrix[(row2 + 1) % 5][col2]
        else:
            return self._matrix[row1][col2] + self._matrix[row2][col1]

    def _decrypt_pair(self, pair):
        row1, col1 = self._get_coordinates(pair[0])
        row2, col2 = self._get_coordinates(pair[1])
        if row1 == row2:
            return self._matrix[row1][(col1 - 1) % 5] + self._matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            return self._matrix[(row1 - 1) % 5][col1] + self._matrix[(row2 - 1) % 5][col2]
        else:
            return self._matrix[row1][col2] + self._matrix[row2][col1]

    def encrypt(self, plaintext: str) -> str:
        plaintext = plaintext.lower().replace("j", "i")
        plaintext = ''.join(filter(str.isalnum, plaintext))
        for i in range(1, len(plaintext)):
            if plaintext[i] == plaintext[i-1] and plaintext[i].isalpha() and plaintext[i] != 'x':
                plaintext = plaintext[:i] + 'x' + plaintext[i:]
        ciphertext = ''
        i = 0
        while i < len(plaintext):
            if not plaintext[i].isalpha():
                ciphertext += plaintext[i]
                i += 1
            else:
                pair = plaintext[i:i+2]
                if len(pair) == 1:
                    pair += 'x'
                    i += 1
                elif not pair[1].isalpha():
                    i += 1
                    plaintext = plaintext[:i] + 'x' + plaintext[i:]
                    pair = plaintext[i:i+2]
                    i -= 1
                ciphertext += self._encrypt_pair(pair)
                i += 2
        return ciphertext

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = ciphertext.lower()
        plaintext = ''
        i = 0
        while i < len(ciphertext):
            if not ciphertext[i].isalpha():
                plaintext += ciphertext[i]
                i += 1
            else:
                pair = ciphertext[i:i+2]
                plaintext += self._decrypt_pair(pair)
                i += 2
        return plaintext


# Example usage:
if __name__ == "__main__":
    key = "secret"
    cipher = PlayfairCipher(key)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
