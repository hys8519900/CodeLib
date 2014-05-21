import hashlib,struct

ver = 2
prev_block = "0000000000000000720a3aa092f3e49e5e3a937ea756966f78ec13c0cf2c36d4"
mrkl_root = "3fa98286e733ad24db368e9306a1553ce7d5d95311ddcc594bef89cea8c96d93"
time_ = 0x536C6DFF #0x53058b35 ->  2014-02-20 04:57:25
bits = 0x1900896c


exp = bits >> 24
mant = bits & 0xffffff
target_hexstr = '%064x' % (mant * (1<<(8*(exp -3))))
target_str = target_hexstr.decode('hex')

nonce =  745234521

while nonce < 0x100000000:
    header = (struct.pack("<L",ver) + prev_block.decode('hex')[::-1] +
              mrkl_root.decode('hex')[::-1] + struct.pack("<LLL",time_,bits,nonce))
    hash = hashlib.sha256(hashlib.sha256(header).digest()).digest()
    print nonce,hash[::-1].encode('hex')
    if hash[::-1] < target_str:
        print 'success'
        break
    nonce += 1
