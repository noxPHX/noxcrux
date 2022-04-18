from django.contrib.auth.hashers import PBKDF2PasswordHasher


class RelievedPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    """
    A subclass of PBKDF2PasswordHasher that uses 130000 iterations for server relief as client side already computed 130000 iterations
    """
    iterations = 130000
