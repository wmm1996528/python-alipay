'''
加密解密 验签
'''
from Cryptodome import Signature
from Cryptodome.Signature import PKCS1_v1_5
from Cryptodome.Cipher import PKCS1_v1_5
from Cryptodome.Hash import SHA, SHA256
from Cryptodome.PublicKey import RSA
from Cryptodome import Random
import base64



PUBKEY = open('app_public_key.pem', 'r', encoding='utf-8').read()
PRIVATEKEY = open('app_private_key.pem', 'r', encoding='utf-8').read()
ALIPAY_KEY = open('alipay_public_key.pem', 'r', encoding='utf-8').read()
# message = 'asdasd'
# #签名
# key = RSA.import_key(PRIVATEKEY)
# h = SHA256.new(message.encode())
# sign = PKCS1_v1_5.new(key).sign(h)
# print(base64.b64encode(sign))#转码方便传递的格式
#
# #验签
#
# key = RSA.import_key(PUBKEY)
# h = SHA256.new(message.encode())
# try:
#     PKCS1_v1_5.new(key).verify(h, sign)
#     print('chenggong')
# except:
#     print('asdasd')

#rsa加密
password = '123456'
key = RSA.import_key(PUBKEY)
cipher = PKCS1_v1_5.new(key)
ciphertext = base64.b64encode(cipher.encrypt(password.encode()))


# rsa解密
key = RSA.import_key(PRIVATEKEY)
dsize = SHA.digest_size
sentinel = Random.new().read(15+dsize)
cipher = PKCS1_v1_5.new(key)
message = cipher.decrypt(base64.b64decode(ciphertext), sentinel).decode()
print(message)
