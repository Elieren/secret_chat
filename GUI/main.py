import os
import customtkinter
import tkinter
import threading
import time
import socket
from cryptography.fernet import Fernet
import win10toast

# Modes: system (default), light, dark
customtkinter.set_appearance_mode("System")
# Themes: blue (default), dark-blue, green
customtkinter.set_default_color_theme("green")

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1200x800")
app.title('Secret Chat')
app.resizable(False, False)

status = 0
text = ''
nickname = ''
key = ''
shift = list()
baza = ''
client = ''

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
    else:
        pass

#------------------------------------------------------------#
rus = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З",
       "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]

eng = ["A", "B", "C", "D", "E", "F", "G",
       "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

probel = [" "]

znaki = [",", ".", "!", "?", '"', "@", "№",
         "#", "$", ";", "%", "^", ":", "&", "*", "(", ")", "-", "_", "+", "=", "{", "}", "[", "]", "'", ">", "<", "/", "\\", "|", "~", "`"]

a = [rus, eng]
for i in a:
    f = list()
    for x in i:
        f.append(x.lower())
    i.extend(f)

over = rus + eng + numbers + probel + znaki
#------------------------------------------------------------#
#CRYPT_V1

def encrypted(massager, baza):
    global over

    text2 = list(massager)

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
        nom = 118
        for n in over[118:128]:
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
    b = b[shift[0]:] + b[:shift[0]]
    b = b[-shift[1]:] + b[:-shift[1]]
    b = b[shift[2]:] + b[:shift[2]]
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
    b = b[-shift[2]:] + b[:-shift[2]]
    b = b[shift[1]:] + b[:shift[1]]
    b = b[-shift[0]:] + b[:-shift[0]]
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

def find():
    a = 0
    while True:
        link = entry.get()
        if link != '':
            if a == 0:
                button.configure(state="normal")
                a = 1
        else:
            if a == 1:
                button.configure(state="disabled")
                a = 0
        time.sleep(0.2)

def pr():
    global text
    global status
    global nickname
    global key
    global shift
    global baza
    global client

    if status == 0:
        nickname = entry.get()
        textbox.delete('0.0', tkinter.END)
        entry.delete(0, tkinter.END)
        textbox.insert('0.0','ip adders server: ')
        status += 1
    elif status == 1:
        ip_server = entry.get()
        textbox.delete('0.0', tkinter.END)
        entry.delete(0, tkinter.END)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip_server, 9090))
        textbox.insert('0.0','key: ')
        status += 1
    elif status == 2:
        key = entry.get()
        textbox.delete('0.0', tkinter.END)
        entry.delete(0, tkinter.END)
        baza = fornet(key)
        textbox.insert('0.0','transitions: ')
        status += 1
    elif status == 3:
        shif = entry.get()
        for x in shif:
            x = int(x)
            shift.append(x)
        textbox.delete('0.0', tkinter.END)
        entry.delete(0, tkinter.END)
        status += 1
        message = '{}'.format(nickname)
        cod = encrypted(message, baza)
        cod_v2 = encrypted_V2(cod)
        cod_v3 = encrypted_V3(cod_v2)
        client.send(cod_v3)
    else:
        messager = entry.get()
        message = '{}: {}'.format(nickname, messager)
        cod = encrypted(message, baza)
        cod_v2 = encrypted_V2(cod)
        cod_v3 = encrypted_V3(cod_v2)
        client.send(cod_v3)
        entry.delete(0, tkinter.END)

def receive():
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
                        nicknameup = nickname
                        if nick[0] == nicknameup:
                            textbox.insert(tkinter.END, f'🟢{message}\n')
                            test = b''
                        else:
                            textbox.insert(tkinter.END, f'{message}\n')
                            test = b''
                    except:
                        textbox.insert(tkinter.END, f'{message}\n')
                        test = b''
                except:
                    textbox.insert(tkinter.END, '🔴 ALARM 🔴')
                    test = b''
            except:
                if (message == b'^ Connect ^') or (message == b'^ left! ^'):
                    text_byte = message.decode('utf-8')
                    textbox.insert(tkinter.END, f"{text_byte}\n")
                    test = b''
                else:
                    pass
        except:
            time.sleep(0.5)


textbox = customtkinter.CTkTextbox(master=app, width=250)
textbox.place(relx=0.5, rely=0.43, anchor=tkinter.CENTER, width=1100, height=650)

textbox.insert('0.0','Nickname: ')

entry = customtkinter.CTkEntry(master=app, placeholder_text="message", font=("Arial Bold", 25))
entry.place(relx=0.45, rely=0.9, anchor=tkinter.CENTER, width=800)

button = customtkinter.CTkButton(master=app, text='button', state="disabled", command=pr, font=("Arial Bold", 25))
button.place(relx=0.85, rely=0.9, anchor=tkinter.CENTER)

t1 = threading.Thread(target=find)
t1.start() 

t2 = threading.Thread(target=receive)
t2.start()


app.mainloop()