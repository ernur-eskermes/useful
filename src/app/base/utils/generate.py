import random

chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyz' \
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'


def generate_pass(length: int = 12) -> str:
    string = ''
    for i in range(length):
        string += random.choice(chars)
    return string


def generate_email(email: str) -> str:
    return 'test_' + email
