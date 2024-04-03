"""
 #  num-muti :: bet-lam 打函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of deps builtin numer-python
"""

from .__deps__ import *
def Sam_shp(     ox:TYP[41]):
    assert (ist( ox,TYP[41]))
    aqh_shp  = [_ex.shape for _ex in ox]
    return  len(set(aqh_shp)) == 1