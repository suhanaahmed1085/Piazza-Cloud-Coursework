from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()

# for when signing up 
def hash_password(password: str) -> str:
    return password_hasher.hash(password)

# for when logging in 
def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)