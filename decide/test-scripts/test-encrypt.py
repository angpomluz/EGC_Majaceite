#!/usr/bin/env python

import sys
from mixnet.mixcrypt import MixCrypt
from mixnet.mixcrypt import ElGamal


PK = sys.argv[1]
MSG = sys.argv[2]
# cambiar      V   por int si no funciona con str
p, g, y = map(str, PK.split(','))
k = MixCrypt(bits=256)
k.k = ElGamal.construct((p, g, y))

print(','.join(map(str, k.encrypt(int(MSG)))))
