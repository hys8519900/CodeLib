import ecdsa
import ecdsa.der
import ecdsa.util
import hashlib
import os
import re
import struct

#import math

b58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58encode(n):
    result = ''
    while n > 0:
        result = b58[n%58] + result
        n /= 58
    return result

def base256decode(s):
    result = 0
    for c in s:
        result = result * 256 + ord(c)
    return result

def countLeadingChars(s, ch):
    count = 0
    for c in s:
        if c == ch:
            count += 1
        else:
            break
    return count

# https://en.bitcoin.it/wiki/Base58Check_encoding
def base58CheckEncode(version, payload):
    s = chr(version) + payload
    checksum = hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4]
    result = s + checksum
    leadingZeros = countLeadingChars(result, '\0')
    return '1' * leadingZeros + base58encode(base256decode(result))

def privateKeyToWif(key_hex):    
    return base58CheckEncode(0x80, key_hex.decode('hex'))
    
def privateKeyToPublicKey(s):
    sk = ecdsa.SigningKey.from_string(s.decode('hex'), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    return ('\04' + sk.verifying_key.to_string()).encode('hex')
    
def pubKeyToAddr(s):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(hashlib.sha256(s.decode('hex')).digest())
    return base58CheckEncode(0, ripemd160.digest())

def keyToAddr(s):
    return pubKeyToAddr(privateKeyToPublicKey(s))

def base256encode(n):
    result = ''
    while n > 0:
        result = chr(n%256) + result
        n /= 256
    return result

def base58decode(s):
    result = 0
    for c in s:
        result = result * 58 + b58.find(c)
    return result

#------------------------------------------------------------------------------#
#from python-bitcoin-client
__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)


def b58encode(v):
    """ encode v, which is a string of bytes, to base58.        
    """

    long_value = int(v.encode("hex_codec"), 16)

    result = ''
    while long_value >= __b58base:
        div, mod = divmod(long_value, __b58base)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in v:
        if c == '\0': nPad += 1
        else: break
    print nPad
    return (__b58chars[0]*nPad) + result

def b58decode(v, length):
    """ decode v into a string of len bytes
    """

    long_value = 0L
    for (i, c) in enumerate(v[::-1]):
        long_value += __b58chars.find(c) * (__b58base**i)
    
    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result

    nPad = 0
    for c in v:
        if c == __b58chars[0]: nPad += 1
        else: break

    result = chr(0)*nPad + result
    if length is not None and len(result) != length:
        return None

    return result

def sha_256(data):
        return hashlib.sha256(data).digest()

def ripemd_160(data):
        return hashlib.new("ripemd160", data).digest()

def hash_160(public_key):
        h1 = sha_256(public_key)
        h2 = ripemd_160(h1)
        return h2

def bc_address_to_hash_160(addr):
        bytes = b58decode(addr,25)
        return bytes[1:21]
#------------------------------------------------------------------------------#
def getHash_addrFromRawTx(tx):
        nh = tx.find('76a914')
        nt = tx.find('88ac')
        if (nh == -1) or (nt == -1):
                return ''
        else:
                return tx[nh+6:nt]
        
def base58en(s):
    return base58encode(base256decode(s))

def base58de(s58):
    return base256encode(base58decode(s58))

def base58CheckDecode(s58):
    return base58de(s58).encode('hex')[2:-8].decode('hex')

def base58CheckDumpDecode(s58):
    #for WIF dumpprikey (add0x01) to random 265bit private key
    return base58de(s58).encode('hex')[2:-10].decode('hex')

def checksum(s):
    #need decode('hex')
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()[0:4].encode('hex')
#--------------------------------
def printCpriToHash160(s):
    temp = base58CheckDumpDecode(s).encode('hex')
    temp = privateKeyToPublicKey(temp)
    print hash_160(temp.decode('hex')).encode('hex')

# Generate a random private key
private_key = '18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725'
# You can verify the values on http://brainwallet.org/
#print "Secret Exponent (Uncompressed) : %s " % private_key 
#print "Private Key     : %s " % privateKeyToWif(private_key)
#print "Address         : %s " % keyToAddr(private_key)
#print base58encode(base256decode(s)) base58en(s) or b58encode()
#print base256encode(base58decode(s58)) Decode58 or b58decode(v,length)
address = '19XxWuKpjubhxazjALPNTEbBYm4BkdExG5'
dumpprivkey = 'KyCLtTLTruGixW16AHVdNfN5zckXp1ELXKo8HhbiSg5ct2n6bjC8'
tx = '01000000013210f0964c78457db4c3cd23b16ddcc94d9284794f2a561bda0aaed2079206bc000000006a473044022037997da56f197799617036d3a98c1d991f77ba9275180c574bfda3dbedf44ad102206a7fdfb7c5c1b0a071aa0bf8f32e3956be1c3c8508f901c79a11e2c8497a692701210219bc50ee4766c82a0b8356dd7fec1cb9abee59958e8f0ab6235058e17276bf6dffffffff02e0c20f24010000001976a914e16e628e86a2651bca15da8ee77e9e0c9a6d06ff88ac00e1f505000000001976a9145d9bd3c1babf85cd314ad55ec898d37a93456a9088ac00000000'
dumpprivkey2 = '5KehCbbxxMsPomgbYqJf2VXKtiD8UKVuaHStjaUyRsZ1X2KjmFZ'
test1 = '5HwoXVkHoRM8sL2KmNRS217n1g8mPPBomrY7yehCuXC1115WWsh'
test2 = 'KwntMbt59tTsj8xqpqYqRRWufyjGunvhSyeMo3NTYpFYzZbXJ5Hp'
secret = '1111111111111111111111111111111111111111111111111111111111111111'

t = '803af8b1c4c5f6316581639754aecf5cd8aa0e03b705711c012f983f4163f5f3b8'
print checksum(t.decode('hex'))
t = t+checksum(t.decode('hex'))
print base58en(t.decode('hex'))
