from passlib.hash import bcrypt
def hash_the_password(password):
    hash_password=bcrypt.hash(password)
    return hash_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(plain_password, hashed_password)