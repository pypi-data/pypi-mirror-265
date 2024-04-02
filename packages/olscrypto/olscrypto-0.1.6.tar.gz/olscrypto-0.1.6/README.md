```python
from olscrypto import Decryptor

SEEDKEY = '<your key>'
dec = Decryptor(SEEDKEY)
dec.decryptfile(<encrypted file>,<decrypted file>)
dec.unzip(<decrypted file>,<target folder>)
```
