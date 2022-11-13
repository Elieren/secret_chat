# secret_chat
This is a chat with three levels of encryption.

### Сreate encryption keys
```
python3 key_gen.py
```

The __key:__ will be displayed

A __key.py__ file will also be created

### Start client

Put the key file in the same directory as the client file.

```
python3 client.py
```

Enter any three-digit number in the "transitions" field.

## __!__
__This must be repeated for all users.__

__All users must have the same key and file.__

__The "transitions" field must have the same number for all clients in order for the program to work correctly.__

### Start server
```
python3 server.py
```

__Default port 9090__
