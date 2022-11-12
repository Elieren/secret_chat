import socket
import threading
from cryptography.fernet import Fernet
import platform
import os
import win10toast

# Choosing Nickname
nickname = input("Choose your nickname: ")

ip_server = str(input('ip_server: '))

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip_server, 9090))

key = str(input('key: '))
shift = int(input('transitions: '))

plat = platform.processor()

if plat == '':
    pushed = 0
else:
    lord = input('Push (Y/N): ')
    lord = lord.upper()
    if lord == 'Y':
        pushed = 1
    elif lord == 'N':
        pushed = 0

print('\n')

#------------------------------------------------------------#

def fornet(key):
    from key import KEY
    baza = KEY
    em = Fernet(key).decrypt(baza)
    em = em.decode('utf-8')
    baza = em.split(" ")
    return baza

def push(message):
    title = "New message"
    plt = platform.system()
    if plt == "Darwin":
        command = f'''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
        os.system(command)
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
        os.system(command)
    elif plt == "Windows":
        win10toast.ToastNotifier().show_toast(title, message, duration=4)
        return
    else:
        return

#------------------------------------------------------------#
rus = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З",
       "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]

eng = ["A", "B", "C", "D", "E", "F", "G",
       "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

probel = [" "]

znaki = [",", ".", "!", "?", '"', "@", "№",
         "#", "$", ";", "%", "^", ":", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "'", ">", "<", "/", "\\", "|", "~", "`"]

over = rus + eng + numbers + probel + znaki
#------------------------------------------------------------#
#CRYPT_V1
baza = fornet(key)

def encrypted(massager, baza):
    global over

    text = massager.upper()

    text2 = list(text)

    cod = ""

    for x in text2:
        nom = 0
        for r in over:
            if x in r:
                cod = cod + f"{baza[nom]}"
            else:
                pass
            nom += 1

    low = len(cod)
    low = str(low)
    cod = cod + "|"

    for x in low:
        nom = 59
        for n in over[59:69]:
            if x in n:
                cod = cod + f"{baza[nom]}"
            else:
                pass
            nom += 1

    text2.clear()
    return cod

def decrypted(message, baza):

    global over

    text2 = list()
    ty = ""
    text = ""
    c = 0
    cod = ""
    cop = ''

    key = message.split("|")

    lop = len(key[0])
    lor = (key[0])

    lof = (key[1])
    n = 5
    text5 = [lof[i:i+n] for i in range(0, len(lof), n)]

    for x in text5:
        nom = 0
        for b in baza:
            if b in x:
                cop = cop + f"{over[nom]}"
            else:
                pass
            nom += 1
    lop = str(lop)

    if lop == cop:
        n = 5
        text2 = [lor[i:i+n] for i in range(0, len(lor), n)]

        for x in text2:
            nom = 0
            for b in baza:
                if b in x:
                    cod = cod + f"{over[nom]}"
                else:
                    pass
                nom += 1
    else:
        cod = '🔴 ALARM 🔴'
    message = cod
    return message
#-----------------------------------------------------#
#CRYPT_V2

def encrypted_V2(cod):
    a = []
    b = []
    d = 0
    global shift
    for x in cod:
        a.append(x)
    l = len(a)
    while d < l:
        b.append(a[0])
        del a[0]
        d += 1
        try:
            b.append(a[-1])
            del a[-1]
            d += 1
        except:
            continue
    b = b[shift:] + b[:shift]
    b = ("".join(b))
    return b

def decrypted_v2(message_v3):
    e = 0
    g = 0
    b = []
    c = []
    global shift
    for x in message_v3:
        b.append(x)
    b = b[-shift:] + b[:-shift]
    l = len(b)
    while e < l:
        try:
            c.append(b[g])
            g += 2
            e += 1
        except:
            e += 1
            continue
    e = 0
    if (l % 2) != 0:
        g = 2
    else:
        g = 1
    while e < l:
        try:
            c.append(b[-g])
            g += 2
            e += 1
        except:
            e += 1
            continue
    c = ("".join(c))
    return c

#---------------------------------------------------#
#CRYPT_V3

def encrypted_V3(cod_v2):
    message = cod_v2.encode('utf-8')
    cod_v3 = Fernet(key).encrypt(message)
    return cod_v3

def decrypted_V3(message):
    message_v3 = Fernet(key).decrypt(message)
    return message_v3

#======================================================#
message = '{}'.format(nickname)
cod = encrypted(message, baza)
cod_v2 = encrypted_V2(cod)
cod_v3 = encrypted_V3(cod_v2)
client.send(cod_v3)
#======================================================#

def receive(pushed):
    test = b''
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024)
            test += message
            try:
                message_v3 = decrypted_V3(test)
                try:
                    message_v3 = message_v3.decode('utf-8')
                    message_v2 = decrypted_v2(message_v3)
                    try:
                        message = decrypted(message_v2, baza)
                        nick = message.split(":")
                        nicknameup = nickname.upper()
                        if nick[0] == nicknameup:
                            test = b''
                        else:
                            print(message.lower())
                            test = b''
                            if pushed == 1:
                                push(message)
                            else:
                                pass
                    except:
                        print(message_v2)
                        test = b''
                        if pushed == 1:
                            push(message)
                        else:
                            pass
                except:
                    print('🔴 ALARM 🔴')
                    test = b''
            except:
                if (message == b'^ Connect ^') or (message == b'^ left! ^'):
                    print(message.decode('utf-8'))
                    test = b''
                else:
                    pass
        except:
            pass

def write():
    while True:
        messager = input(': ')
        message = '{}: {}'.format(nickname, messager)
        cod = encrypted(message, baza)
        cod_v2 = encrypted_V2(cod)
        cod_v3 = encrypted_V3(cod_v2)
        client.send(cod_v3)

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive, args=(pushed,))
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()