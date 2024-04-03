"""
 #  bas-muti :: ini-lam 初函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of init builtin numer-python
"""

from .depLam import *
# ARES FIXME : nan; 
def initMod(_nn_mod, _nn_ini_):
  _nn_ini_['bia'](_nn_mod.bias.data)
  _nn_ini_['wei'](_nn_mod.weight.data)
  return _nn_mod

# [22W12] ARES
def initMod_ran( ox:TYP[60]):
  for m in  ox.modules():
    if ist(m, nmb.nn.Conv2d):
      nmb.nn.init.xavier_normal_(m.weight.data)
      #nn.init.kaiming_normal_(m.weight, mode='fan_in', nonlinearity='relu')
      if m.bias is not None:
        m.bias.data.zero_()
        #nn.init.constant_(m.bias, 0)
    elif ist(m, nmb.nn.BatchNorm2d):
      m.weight.data.fill_(1)
      m.bias.data.zero_()
      #nn.init.constant_(m.bias, 0)
    elif ist(m, nmb.nn.Linear):
      nmb.nn.init.normal_(m.weight.data, 0, 0.01)
      # m.weight.data.normal_(0,0.01)
      m.bias.data.zero_()

if  bas.Her(__name__):
    print('beol')