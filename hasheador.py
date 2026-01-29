from argon2 import PasswordHasher

ph = PasswordHasher()

password = input("Enter password: ").encode('utf-8')
res = ph.hash(password)
print("hash: ", res)

try:
    pass2 = input("Enter password to verify: ").encode('utf-8')
    ph.verify(res, pass2)
    print("Password match!")
    res2 = ph.hash(pass2)
    print("has2: ", res2)
except Exception:
    print("Incorrect password.")