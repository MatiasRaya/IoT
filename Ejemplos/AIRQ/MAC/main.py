import binascii
var1 = b'E5A13BAA8BC1'
var2 = b'C4E7C34D76D3'
var3 = b'DDEBAC222089'
var4 = b'C45F20212AAC'
var5 = b'DCE84B5BA2BD'
var6 = b'CAADBB95E129'
var7 = b'EA754361BFEB'
var8 = b'D5246DE3B0DA'

print("AIRQ1: {}".format(binascii.unhexlify(var1)))
print("AIRQ2: {}".format(binascii.unhexlify(var2)))
print("AIRQ3: {}".format(binascii.unhexlify(var3)))
print("AIRQ4: {}".format(binascii.unhexlify(var4)))
print("AIRQ5: {}".format(binascii.unhexlify(var5)))
print("AIRQ6: {}".format(binascii.unhexlify(var6)))
print("AIRQ7: {}".format(binascii.unhexlify(var7)))
print("AIRQ8: {}".format(binascii.unhexlify(var8)))

print()
print()
print()

print("AIRQ1: {}".format(int.from_bytes(binascii.unhexlify(var1),"little")))
print("AIRQ2: {}".format(int.from_bytes(binascii.unhexlify(var2),"little")))
print("AIRQ3: {}".format(int.from_bytes(binascii.unhexlify(var3),"little")))
print("AIRQ4: {}".format(int.from_bytes(binascii.unhexlify(var4),"little")))
print("AIRQ5: {}".format(int.from_bytes(binascii.unhexlify(var5),"little")))
print("AIRQ6: {}".format(int.from_bytes(binascii.unhexlify(var6),"little")))
print("AIRQ7: {}".format(int.from_bytes(binascii.unhexlify(var7),"little")))
print("AIRQ8: {}".format(int.from_bytes(binascii.unhexlify(var8),"little")))
