import socket
import threading
from cryptography.fernet import Fernet
import platform
import pickle
# import os
# import win10toast


class Client():

    def __init__(self):
        rus = ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З",
               "И", "Й", "К", "Л", "М", "Н", "О", "П", "Р",
               "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ",
               "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]

        eng = ["A", "B", "C", "D", "E", "F", "G",
               "H", "I", "J", "K", "L", "M", "N",
               "O", "P", "Q", "R", "S", "T", "U",
               "V", "W", "X", "Y", "Z"]

        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        probel = [" "]

        znaki = [",", ".", "!", "?", '"', "@", "№",
                 "#", "$", ";", "%", "^", ":", "&",
                 "*", "(", ")", "-", "_", "+", "=",
                 "{", "}", "[", "]", "'", ">", "<",
                 "/", "\\", "|", "~", "`"]

        for i in [rus, eng]:
            temporary = []
            for x in i:
                temporary.append(x.lower())
            i.extend(temporary)

        self.__full = rus + eng + numbers + probel + znaki

        self.__nickname = input("Choose your nickname: ")
        self.__ip_server = str(input('ip_server: '))

        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self.__ip_server, 9090))

        self.__key_load()
        self.__selection()
        self.__fornet()

        self.__start()

        # Starting Threads For Listening And Writing
        receive_thread = threading.Thread(target=self.__get_message)
        receive_thread.start()

        write_thread = threading.Thread(target=self.__write)
        write_thread.start()

    def __key_load(self):
        self.__key = str(input('key: '))
        self.__transitions = str(input('transitions: '))
        self.__transitions_array = []
        for x in self.__transitions:
            self.__transitions_array.append(int(x))

    def __selection(self):
        self.__plat = platform.processor()

        if self.__plat == '':
            self.__pushed = 0
        else:
            x = input('Push (Y/N): ').upper()
            if x == 'Y':
                self.__pushed = 1
            elif x == 'N':
                self.__pushed = 0

    def __fornet(self):
        with open('file.key', 'rb') as file:
            key = pickle.load(file)
        code = Fernet(self.__key).decrypt(key)
        self.__baza = code.decode('utf-8').split(' ')

    def __push(self):
        pass
        """title = "New message"
        plt = platform.system()
        if plt == "Darwin":
            command = f'''
            osascript -e 'display notification "{self.__message_received}" \
with title "{title}"'
            '''
            os.system(command)
        elif plt == "Linux":
            command = f'''
            notify-send "{title}" "{self.__message_received}"
            '''
            os.system(command)
        elif plt == "Windows":
            win10toast.ToastNotifier().show_toast(
                title, self.__message_received, duration=4)
        else:
            pass"""

    def __encode_level_1(self):
        message = list(self.__message_sending)

        encode_text = ''

        for i in message:
            for x, z in enumerate(self.__full):
                if i in z:
                    encode_text += f"{self.__baza[x]}"
                else:
                    pass

        text_len = str(len(encode_text))
        encode_text += '|'

        for i in text_len:
            x = 118
            for n in self.__full[118:128]:
                if i in n:
                    encode_text += f'{self.__baza[x]}'
                else:
                    pass
                x += 1

        self.__message_sending = encode_text

    def __decode_level_1(self):
        text = str(self.__message_received).split('|')
        length_key = 5
        code_text = text[0]
        len_text = str(len(text[0]))
        key = text[1]

        decode_len = ''
        decode_text = ''

        decode_key = [key[i:i + length_key]
                      for i in range(0, len(key),
                      length_key)]

        for i in decode_key:
            for x, b in enumerate(self.__baza):
                if b in i:
                    decode_len += f"{self.__full[x]}"
                else:
                    pass

        if len_text == decode_len:
            decode_text_key = [
                code_text[i:i + length_key]
                for i in range(0, len(code_text),
                               length_key)]

            for i in decode_text_key:
                for x, b in enumerate(self.__baza):
                    if b in i:
                        decode_text += f"{self.__full[x]}"
                    else:
                        pass

            self.__message_received = decode_text
        else:
            self.__message_received = "Error. The key doesn't fit."

    def __encode_level_2(self):
        char_text = []
        encode_text = []
        i = 0
        t_a = self.__transitions_array
        for x in self.__message_sending:
            char_text.append(x)
        len_text = len(char_text)
        while i < len_text:
            encode_text.append(char_text[0])
            del char_text[0]
            i += 1
            try:
                encode_text.append(char_text[-1])
                del char_text[-1]
                i += 1
            except Exception:
                continue

        encode_text = encode_text[t_a[0]:] + encode_text[:t_a[0]]
        encode_text = encode_text[-t_a[1]:] + encode_text[:-t_a[1]]
        encode_text = encode_text[t_a[2]:] + encode_text[:t_a[2]]
        self.__message_sending = ("".join(encode_text))

    def __decode_level_2(self):
        i = 0
        x = 0
        char_text = []
        decode_text = []
        t_a = self.__transitions_array
        for x in self.__message_received:
            char_text.append(x)

        char_text = char_text[-t_a[2]:] + char_text[:-t_a[2]]
        char_text = char_text[t_a[1]:] + char_text[:t_a[1]]
        char_text = char_text[-t_a[0]:] + char_text[:-t_a[0]]

        len_text = len(char_text)
        x = 0
        while i < len_text:
            try:
                decode_text.append(char_text[x])
                x += 2
                i += 1
            except Exception:
                i += 1
                continue
        i = 0
        if (len_text % 2) != 0:
            x = 2
        else:
            x = 1
        while i < len_text:
            try:
                decode_text.append(char_text[-x])
                x += 2
                i += 1
            except Exception:
                i += 1
                continue
        self.__message_received = ("".join(decode_text))

    def __encode_level_3(self):
        message = self.__message_sending.encode('utf-8')
        self.__message_sending = Fernet(self.__key).encrypt(message)

    def __decode_level_3(self):
        self.__message_received = Fernet(self.__key) \
            .decrypt(self.__message_received)

    def __get_message(self):
        self.__message_received = b''
        while True:
            try:
                # Receive Message From Server
                self.__message_received += self.__client.recv(1024)
                try:
                    self.__decode_level_3()
                    try:
                        self.__message_received = self.__message_received \
                            .decode('utf-8')
                        self.__decode_level_2()
                        try:
                            self.__decode_level_1()
                            nick = self.__message_received.split(":")
                            nicknameup = self.__nickname
                            if nick[0] == nicknameup:
                                self.__message_received = b''
                            else:
                                print(self.__message_received)
                                self.__message_received = b''
                                if self.__pushed == 1:
                                    self.__push()
                                else:
                                    pass
                        except Exception:
                            print(self.__message_received)
                            self.__message_received = b''
                            if self.__pushed == 1:
                                self.__push()
                            else:
                                pass
                    except Exception:
                        print('🔴 ALARM 🔴')
                        self.__message_received = b''
                except Exception:
                    if (self.__message_received == b'^ Connect ^') or (
                            self.__message_received == b'^ leave! ^'):
                        print(self.__message_received.decode('utf-8'))
                        # self.__message_received = b''
                    else:
                        pass
                    self.__message_received = b''
            except Exception:
                pass

    def __write(self):
        while True:
            message = input(': ')
            self.__message_sending = '{}: {}'.format(self.__nickname, message)
            self.__encode_level_1()
            self.__encode_level_2()
            self.__encode_level_3()
            self.__client.send(self.__message_sending)

    def __start(self):
        self.__message_sending = '{}'.format(self.__nickname)
        self.__encode_level_1()
        self.__encode_level_2()
        self.__encode_level_3()
        self.__client.send(self.__message_sending)


if __name__ == '__main__':
    Client()
