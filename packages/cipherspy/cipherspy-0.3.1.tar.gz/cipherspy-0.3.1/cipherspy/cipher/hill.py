import math


class HillCipher:
    def __init__(self, key_iter: iter):
        super().__init__()
        if len(key_iter) == 4:
            self._key_iter = key_iter
        else:
            raise ValueError('key length must be 4')
        det = self._key_iter[0] * self._key_iter[3] - self._key_iter[1] * self._key_iter[2]
        if math.gcd(det, 26) == 1:
            self._det = det
            self._det_inverse = pow(self._det, -1, 26)
        else:
            raise ValueError("The key matrix is not invertible for the given modulus.")

    @property
    def key_iter(self) -> iter:
        return self._key_iter

    @key_iter.setter
    def key_iter(self, key_iter: iter) -> None:
        if len(key_iter) == 4:
            self._key_iter = key_iter
        else:
            raise ValueError('key length must be 4')
        det = self._key_iter[0] * self._key_iter[3] - self._key_iter[1] * self._key_iter[2]
        if math.gcd(det, 26) == 1:
            self._det = det
            self._det_inverse = pow(self._det, -1, 26)
        else:
            raise ValueError("The key matrix is not invertible for the given modulus.")

    def _encrypt_pair(self, pair):
        p1 = chr(ord(pair[0]) - ord('a') + 1)
        p2 = chr(ord(pair[1]) - ord('a') + 1)
        c1 = chr(((ord(p1) * self._key_iter[0] + ord(p2) * self._key_iter[1]) % 26) + ord('a'))
        c2 = chr(((ord(p1) * self._key_iter[2] + ord(p2) * self._key_iter[3]) % 26) + ord('a'))
        return c1 + c2

    def _decrypt_pair(self, pair):
        p1 = chr(ord(pair[0]) - ord('a') + 1)
        p2 = chr(ord(pair[1]) - ord('a') + 1)
        c1 = chr(((self._det_inverse * (ord(p1) * self._key_iter[3] - ord(p2) * self._key_iter[1])) % 26) + ord('a'))
        c2 = chr(((self._det_inverse * (-ord(p1) * self._key_iter[2] + ord(p2) * self._key_iter[0])) % 26) + ord('a'))
        return c1 + c2

    def encrypt(self, plaintext: str) -> str:
        plaintext = ''.join(filter(str.isalnum, plaintext.lower()))
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
    key = (9, 4, 5, 7)
    # key = (9, 5, 2, 4)
    cipher = HillCipher(key)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
