from cipherspy.exceptions import NegativeNumberException


class CaesarCipher:
    def __init__(self, shift: int):
        super().__init__()
        if shift <= 0:
            raise NegativeNumberException(shift)
        self._shift: int = shift % 26

    @property
    def shift(self) -> int:
        return self._shift

    @shift.setter
    def shift(self, shift: int) -> None:
        if shift <= 0:
            raise NegativeNumberException(shift)
        self._shift = shift % 26

    def _shift_char(self, char: chr):
        if char.isalpha():
            shifted = ord(char) + self._shift
            if shifted > ord('z'):
                shifted -= 26
            return chr(shifted)
        return char

    def encrypt(self, plaintext: str) -> str:
        encrypted_text = ''.join([self._shift_char(char) for char in plaintext.lower()])
        return encrypted_text

    def decrypt(self, ciphertext: str) -> str:
        ciphertext = ciphertext.lower()
        self._shift = -self._shift
        decrypted_text = ''.join([self._shift_char(char) for char in ciphertext.lower()])
        self._shift = -self._shift
        return decrypted_text


# Example usage:
if __name__ == "__main__":
    shift = 3
    cipher = CaesarCipher(shift)

    message = "HELLO world 2024"
    print("Original message:", message)

    encrypted_message = cipher.encrypt(message)
    print("Encrypted message:", encrypted_message)

    decrypted_message = cipher.decrypt(encrypted_message)
    print("Decrypted message:", decrypted_message)
