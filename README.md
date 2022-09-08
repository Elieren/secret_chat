# secret_chat
This is a chat with three levels of encryption.

### Сreate encryption keys

`./key_gen.py`

The key and chat will be displayed

A __key.py__ file will also be created

### Write two decryption keys to the client.py
This is the key and chat

`nano client.py`

In "ip_server = ''" insert server ip

In "key = ''" insert key from key_gen
In "chat = ''" insert chat from key_gen

`start client.py`

### !
__This must be repeated for all users.__
__All users must have the same key, chat and file.__

### Start server

`start server.py`