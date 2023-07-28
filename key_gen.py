import random
import string
from cryptography.fernet import Fernet

key = Fernet.generate_key()

print('Key: ', key.decode('utf-8'))

key_arr = []
length = 5

for i in range(163):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    key_arr.append(rand_string)

key_str = ' '.join(key_arr)

key_byte = key_str.encode('utf-8')
key_encripted = Fernet(key).encrypt(key_byte)

key_encripted = key_encripted.decode('utf-8')

f = open('key.py', 'w')
f.write("KEY = b'")
f.write(key_encripted)
f.write("'")
f.close()

from key import KEY
baza = KEY

key_decripted = Fernet(key).decrypt(baza)
key_decripted = key_decripted.decode('utf-8')
key = key_decripted.split(" ")
print('\n', key)
