"""
 #  bas-muti :: deps_basic 公集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  __deps__ builtin basic-python
"""

import os,sys
import pickle
from numbers         import Integral, Real
from argparse        import Namespace
from typing          import Iterable, Optional, Any, Union
from collections.abc import Sequence#, Queue

NON = None
TRU = True
FAL = False


TLA_=[globals(),locals()]

# object
TYP = {
  10: bool,    # char
  11: int,     # uint
  12: float,   # real
  13: complex, # nplx
  14: tuple,   # cbnt
 #20: one-hot,
  21: Integral,
  22: Real,
 #23: Multivar,
 #24: L-Tuple,
  30: set,
  31: Namespace,
  40: str,     # code
  41: list,
  42: dict}

