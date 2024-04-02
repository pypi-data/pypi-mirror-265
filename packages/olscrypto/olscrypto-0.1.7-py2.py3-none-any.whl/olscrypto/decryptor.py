import re
import os
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
import zipfile
IV_LENGTH = 16
ENCODING = 'utf-8'
HEADER_LENGTH = 32
BASEKEY = 'Hive Corp'
unpad = lambda s : s[:-ord(s[len(s)-1:])]
class Decryptor:
    def __init__(self,keystr=BASEKEY):
        if keystr!=None:
            self.key = self.makeKey(keystr)
    def setRawKey(self,keyhex):
        self.key = bytes.fromhex(keyhex)

    def makeKey(self,keystr):
        hashed = sha256(keystr.encode())
        return hashed.digest()
    def unpad(self,byte_array:bytearray):
        return byte_array[:-ord(byte_array[-1:])]
    def decrypt(self, data):
        try:
            enc = bytes.fromhex(data)
        except (UnicodeDecodeError, AttributeError, TypeError):
            enc = data
        # iv = enc[:IV_LENGTH]
        header = enc[:HEADER_LENGTH]
        iv = header[:IV_LENGTH]
        version = header[IV_LENGTH:]
        
        cipher = AES.new(self.key,AES.MODE_CBC, iv)
        decrypted = self.unpad(cipher.decrypt(enc[HEADER_LENGTH:]))
        print('iv',iv.hex(),len(iv))
        print('version',version.hex(),version.decode(),len(version))
        print('key',self.key.hex(),len(self.key))
        return decrypted
    
    def decryptfile(self,encrypted_input,outputfile):
        with open(encrypted_input,'rb') as file:
            ciphertext = file.read()
        decrypted = self.decrypt(ciphertext)
        with open(outputfile,'wb') as file:
            file.write(decrypted) #.encode(ENCODING))
    def unzip(self,file,path):
        with zipfile.ZipFile(file,'r') as zip:
            zip.extractall(path)
    def decryptUnzip(self,encrypted_file,outpath):
        try:
            self.decryptfile(encrypted_file,'tmp.zip')
            self.unzip('tmp.zip',outpath)
            os.remove('tmp.zip')
        except Exception as err:
            print('Error:{}'.format(err))
            raise