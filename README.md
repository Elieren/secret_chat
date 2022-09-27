# secret_chat
This is a chat with three levels of encryption.

### Сreate encryption keys
```
./key_gen.py
```
The key and chat_key will be displayed

`python3 key_gen.py`

The __key:__ and __chat:__ will be displayed

A __key.py__ file will also be created

### Start client

Put the key file in the same directory as the client file.
`nano client.py`

In "  ip_server = ' '  " insert server ip

In "  key = ' '  " insert key from key_gen

In "  chat = ' '  " insert chat from key_gen

`python3 client.py`

```
start client.py
```
## __!__
__This must be repeated for all users.__
__All users must have the same key, chat and file.__

### Start server
```
start server.py
```

`python3 server.py`

__Default port 9090__
