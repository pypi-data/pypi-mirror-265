"""
 #  num-muti :: dep-lam 依函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of deps builtin numer-python
"""

from .__deps__ import *


# 主要是激活函数名
_JC_NYM=dict(
    tah='tanh',
    ath='atanh',
    rlu='relu',
    elu='elu',
    slu='selu',
    clu='silu',
    llu='leaky_relu',
    spl='softplus',
    sig='sigmond',  
    con='conv1d',
    c2n='conv2d',
    c3n='conv3d',
    lin='linear'
)

_NA_LAS_ = {
   'lin' :  nmm.Linear ,
   'c1n' :  nmm.Conv1d ,
   'c2n' :  nmm.Conv2d ,
   'c3n' :  nmm.Conv3d }

#cal= nmm.init.calculate_gain,
_NNiLAM_ = {
   'coe' :  nmm.init.eye_,
   'co1' :  nmm.init.ones_,
   'co0' :  nmm.init.zeros_,
   'drc' :  nmm.init.dirac_,
   'spr' :  nmm.init.sparse_,
   'cns' :  nmm.init.constant_,
   'otg' :  nmm.init.orthogonal_,
   'trn' :  nmm.init.trunc_normal_,
   'xvn' :  nmm.init.xavier_normal_,
   'xvu' :  nmm.init.xavier_uniform_,
   'kmn' :  nmm.init.kaiming_normal_,
   'kmu' :  nmm.init.kaiming_uniform_,
   'ng0' :  nmm.init._no_grad_zero_,
   'ngf' :  nmm.init._no_grad_fill_,
   'ngn' :  nmm.init._no_grad_normal_,
   'ngu' :  nmm.init._no_grad_uniform_,
   'ngt' :  nmm.init._no_grad_trunc_normal_ }

# value foRmat
_NN_NLR_ = {
   'nrm' :  nmm.LayerNorm
}


# str -> activation https://zhuanlan.zhihu.com/p/108603544 https://blog.csdn.net/weixin_38649779/article/details/127647257
_NN_NLA_= dict(
    #ass =pass,
    tah = nmm.Tanh(),
    rlu = nmm.ReLU(),
    llu = nmm.LeakyReLU(),
    plu = nmm.PReLU(),
    elu = nmm.ELU(),
    slu = nmm.SELU(),
    clu = nmm.SiLU(),
    sig = nmm.Sigmoid(),
    spl = nmm.Softplus(),
    # for silly developers:
    tanh= nmm.Tanh(),
    relu= nmm.ReLU(),
    selu= nmm.SELU(),
    silu= nmm.SiLU(),
    leaky_relu= nmm.LeakyReLU(),
    sigmoid   = nmm.Sigmoid(),
    softplus  = nmm.Softplus()
)



def getrJCN(_fc):
  return _JC_NYM[_fc]

def getrNLA(_jc):
  return _NN_NLA_[_jc]

def getrNLR(_jc):
  return _NN_NLR_[_jc]

def getrNPI(_jc):
  return _NNiLAM_[_jc]

def rGai_fnn(tfg):
  nym = tfg['nym'][:3]
  if    nym in set(['ass', 'lin', 'con', 'sig']):
    return  1
  elif  nym in set(['tah', 'rlu', 'llu', 'slu']):
    return nmm.init.calculate_gain(_JC_NYM[nym])  # tfg['par']
  else:
    return 0   # FIXME
  
if  bas.Her(__name__):
    print(getrNPI('coe'))