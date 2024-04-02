from abc import ABC,  abstractmethod

class BaseEncryptor(ABC):
    """
    Provides a common interface for creating concrete encryptor classes.

    :param password: The plaintext password provided by the user.
    :type password: bytes
    """

    def __init__(self, password: bytes) -> None:
        #: The plaintext password.
        self.password = bytes(password, encoding="utf-8")
    
    @abstractmethod
    def encrypt():
        """
        Given data as bytes, encrypt it. Must be implemented by a concrete Encryptor class.
        """
        raise NotImplementedError("An encryptor subclassing BaseEncryptor must define an encrypt() method.")

    @abstractmethod
    def decrypt():
        """
        Given data as bytes, decrypt it. Must be implemented by a concrete Encryptor class.
        """
        raise NotImplementedError("An encryptor subclassing BaseEncryptor must define a decrypt() method.")