import bcrypt


# function to hash
def hashstr(password, salt):
    pwbytes = password.encode("utf-8")
    return bcrypt.hashpw(pwbytes, salt)


# function to salt
def get_salt():
    return bcrypt.gensalt()
