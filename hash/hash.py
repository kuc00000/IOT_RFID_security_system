import hashlib


def hash_function(string):
    hash_ = hashlib.sha256()
    string = string.encode('utf-8')
    hash_.update(string)
    hash_value = hash_.hexdigest()
    return hash_value

