from secrets import token_urlsafe

BASE_LEN: int = 6

def hasher(hash_len: int = BASE_LEN):
    return token_urlsafe(hash_len)
