#!/usr/bin/env python

import sys
from mixnet.mixcrypt import MixCrypt
from mixnet.mixcrypt import ElGamal


SK = sys.argv[1]
MSG = sys.argv[2]
# cambiar         V   por int si no funciona con str
#p, g, y, x = map(str, SK.split(',')) < original
#a, b = map(int, MSG.split(',')) < original
x = map(str, SK.split(','))
y = map(str, SK.split(','))
g = map(str, SK.split(','))
p = map(str, SK.split(','))

b = map(int, MSG.split(','))
a = map(int, MSG.split(','))

k = MixCrypt(bits=256)
k.k = ElGamal.construct((p, g, y, x))

print(k.decrypt((a, b)))
