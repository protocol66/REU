from OU import OU, OUIntegerGroup
from datetime import datetime

msg = -2
msg2 = 10

group = OUIntegerGroup()
ou = OU(group)

pk, sk = ou.keygen()

start = datetime.now()
msg_cipher = ou.encryptWithNeg(pk, sk, msg)
end = datetime.now()
print("Encryption:", end-start)
msg2_cipher = ou.encryptWithNeg(pk, sk, msg2)


cipher_add = msg_cipher + msg2_cipher
cipher_mul = msg_cipher * msg2

start = datetime.now()
decrypted = ou.decrypt(pk, sk, msg_cipher)
end = datetime.now()
print("Decryption:", end-start)

add_decrypt = ou.decrypt(pk, sk, cipher_add)
mul_decrypt = ou.decrypt(pk, sk, cipher_mul)
print("Add: ", add_decrypt)
print("Mul: ", mul_decrypt)
