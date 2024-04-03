"""
 #  num-muti :: deps_numer 公集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  __deps__ builtin numer-python 蟒算
"""
# r

import basic as bas
import os
from numbers         import Integral, Real
from typing          import TypedDict, Iterable, Optional, Any, Union, Sequence#, Queue
#FrozenDict ImmutableDict
from frozendict      import frozendict
# s
NON  =  None
TRU  =  True
FAL  = False
TYP  =  bas.TYP.copy()
# FIXME Jax
_fc  =   os.getenv( 'FC_IMP')
if  bas.ist(_fc,NON) or _fc== '': _fc='tn'
if 'j' in _fc:
    import jax       as nmb
    import jax.numpy as nmp
    import jax.nn    as nmm
if 'h' in _fc:
    pass
    #import haiku     as nmm
if 't' in _fc:
    import torch     as nmb
    import torch.nn  as nmm
if 'n' in _fc:
    import numpy     as nmp

TYP[50] = nmp.ndarray
TYP[51] = nmb.Tensor
TYP[60] = nmm.Module
#TYP     = TypedDict('TYP', TYP)
TYP     = frozendict(TYP)
Unm_sox = Union[TYP[51],TYP[60]]

# t
ist     = bas.ist
'''
def setnImp(_fc='j'):
  if bas.ist(_fc,NON) or _fc== '': _fc='tn'
  if 'j' in _fc:
    import jax       as nmb
    import jax.numpy as nmp
    import jax.nn    as nmm
  if 'h' in _fc:
    import haiku     as nmm
  if 't' in _fc:
    import torch     as nmb
    import torch.nn  as nmm
  if 'n' in _fc:
    import numpy     as nmp
setnImp( os.getenv( 'FC_IMP'))
'''

#tmod = lambda x: nmb.transform(x) if else
#t1   = lambda y: y
    
if bas.Her(__name__):
    print('ddd')