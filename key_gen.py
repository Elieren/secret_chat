import random
import string
from cryptography.fernet import Fernet

chat = Fernet.generate_key()

key = Fernet.generate_key()

print('Key: ',key)

a = 1
g = list()
length = 5

while a < 102:
	    letters_and_digits = string.ascii_letters + string.digits
	    rand_string = ''.join(random.sample(letters_and_digits, length))
	    g.append(rand_string)
	    a += 1


print('\nChat: ',chat)

g = ' '.join(g)

m = g.encode('utf-8')
en = Fernet(key).encrypt(m)

en = en.decode('utf-8')

f = open('key.py', 'w')
f.write("KEY = b'")
f.write(en)
f.write("'")
f.close()

from key import KEY
baza = KEY

print('\n',baza)
#en = baza.decode('utf-8')
em = Fernet(key).decrypt(baza)
em = em.decode('utf-8')
lokey = em.split(" ")
print('\n',lokey)

input()