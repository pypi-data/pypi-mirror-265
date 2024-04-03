"""
 #  转换函数 shf-lams
 @  E.C.Ares
 !  MIT LICENSE
 `  built in pkp for pyTorch tensor
"""
# r(import-refs)
#       r.. im
from .iniLam import *
#       r.. as
pass
# s
_JC_NYM = 'lam_shf'
# to.() = 畨 娄
_KY_    = ['dtype','device']
_LC_TAN = ['train','drop','tre']#,TYP[60].train]
_LC_RAN = ['tests','eval','vlu']#,TYP[60].eval ]
_LC3DEV = ['cpu', 'cud', 'gpu']
_LC3REV = ['otg', 'non']
_LC3PEV = ['rut', 'cut']


# 作用于张量 (Tensor) 的方法
"""
# _apply(lam) 内部会执行3步:
对self.children() 进行递归的调用；
使用fn对 self._parameters 中的参数及其 gradient 进行处理；
使用fn对 self._buffers 中的 buffer 进行处理。
"""
# CHECK: if module changed FIXME: outfile 
def Lam_mod( ox:TYP[60], am):
    if   am  in _LC_TAN: ox.train(  )
    elif am  in _LC_RAN: ox.eval(   )
    elif ist(am, 'lam'): ox.apply(am) # 模型的训练/评估模式，区别于Tensor.apply()
    else:  raise NotImplementedError

def loadMod( ox:TYP[60], lc, *c,**g):
    # TODO map_location strict
    try:
      ox.load_state_dict(
                nmb.load(lc, map_location='cuda'), strict=TRU)
    except: print(f"[{_JC_NYM} | mod] : no-use {lc}")

# TODO Place Params
def tʃumMod( ox:TYP[60], lc):
    nmb.save(ox, lc)
    print(f"[{_JC_NYM} | [T]mod.mPrm] : savt {lc}")

LaiXPrm = dict(
  otg   = None,
  non   = initMod_ran
)

#re-set parameters of mod by ptr else _fc
def LaiRMod(mod, fc, mm='cuda',_fb=False):
    print(f"[{_JC_NYM} | mod] : load {mod._jc} by { fc}")
    if fc in _LC3REV: LaiXPrm[ fc](mod)
    else:
      _lc = bas.Pth(fc)
      _mm = mm if len(mm) <= 4 else mm[:4] 
      loadMod(mod,_lc,_mm)

def LaiPMod( ox:TYP[60], fc, fb=TRU):
    if fb :  ox= ox.state_dict() # 只存其参
    if fc[:3]in _LC3PEV:
            _lc=bas.Pth(fc[:3]) + fc[3:] # FIXME
    else  : _lc=bas.Pth( fc, TRU) # os.makedirs(os.path.dirname(_fc))
    try   : tʃumMod( ox,_lc)
    except: print(f"[{_JC_NYM} | [E]mod.mPrm] : not-dir {_lc}")

# 更改设备放置 memory <-> cpu, cuda <-> cpu, cuda
def Lai_Mod( ox:TYP[60], fh    ):
    if      bas.iseKDic( fh,'m'):
      if fh['d'][:3] in _LC3DEV :
            LaiRMod( ox, fh['m'],fh['d'])
      else: LaiPMod( ox, fh['m'])
    else:
        _ox= ox.detach()
        _fh=fmrtDmm(     fh)
        Dmm_sor(    _ox, fh)

#def Lar_sor( ox:nmm.Module,      ai): #更改数据类型
#模型的行略  更改[张量]所在ノ畨(田置): 栗: .to( ), .save( ), .load( )
def Dmm_sor( ox:Unm_sox, fh={'D':'m'}):
    ox.to(**fmrtDmm(fh))
# 更改数据组织形式，而不是数
def shftLanDdic( ox:Any, fh={'t':NON}):
    ret = {}
    if  ist(ox, NON): return ret
    #if ist(ox, str): FIXME elif
    if 'int' in  ox:  ret[_KY_[0]] = nmb.int32
    else           :  ret[_KY_[0]] = nmb.float32     # if 'float' in dmm
    if 'cpu' in  ox:  ret[_KY_[1]] = nmb.device('cpu')
    else           :  ret[_KY_[1]] = nmb.device('cuda' if nmb.cuda.is_available() else 'cpu')
    return ret

# TODO layout
def fmrtDmm( fx):
    _fh_Dmm= fx if ist( fx,TYP[42]) else shftLanDdic(fx)
    if _fh_Dmm['t'] == 'm': return _fh_Dmm
    _fh_Dmm.setdefault(_KY_[0],nmb.float32) 
    _fh_Dmm.setdefault(_KY_[1],nmb.device('cuda' if nmb.cuda.is_available() else 'cpu')) 
    return _fh_Dmm

def shftLai( ox, fh): return ox.to(**fmrtDmm(fh))

def shftLarTNum( ox:nmb.Tensor): return ox.detach().cpu().numpy()
tsr =  lambda x,dt:nmb.as_tensor(x) if dt is None else nmb.tensor(x, dtype=dt)

#def shftLar_num(ox): return ox.detach().cpu().numpy()
def shftLar_Num( ox:Any, fh={'t':NON}):
    # FIXME
    if      ist( ox,NON    ):return NON
    _fc_typ= fh['t']
    if      ist( ox,TYP[30]):return shftLarTNum(ox).astype(_fc_typ) if _fc_typ else shftLarTNum(ox)
    if      ist( ox,TYP[20]):return ox.astype(_fc_typ)  if _fc_typ else ox
    if      ist( ox,TYP[10]):return ox
    # namedtuple
    if      ist( ox,'it'   ):return type(ox)(*[shftLar_Num(ex, fh) for ex in ox])
    if      ist( ox,TYP[14],
                    TYP[41]):return None if  len( ox) == 0 else [shftLar_Num(ex, fh) for ex in ox]
    if      ist( ox,TYP[42]):return {k:shftLar_Num(ex, fh) for k, ex in ox.items()}
    if      ist( ox,   'sc'):return nmp.array(ox)
    raise TypeError("not support item type: {}".format(type(ox)))
def toN( *c,**g): return shftLar_Num( *c,**g)


# ik ignore key
def shftLar_Tsr( ox:Any, dt:Optional[nmb.dtype] = None, ik: list = ['SCL'], gk=[], fb=False):
    # FIXME
    if      ist( ox,NON    ):return NON
    if      ist( ox,TYP[51]):return      ox.to(  dt) if dt is not None else ox
    if      ist( ox,TYP[42]):return bas.typ( ox)((k,toT(v, dt, ik)) for k,v in ox.items()) if fb\
                               else Tsr_Dix(     {k:toT(v, dt, ik)  for k,v in ox.items()}, gk)
    if      ist( ox,'it'   ):return bas.typ( ox)( *[toT(t, dt)      for t   in ox])
    if      ist( ox,TYP[41],
                    TYP[14]):return bas.typ( ox)([]) if  len( ox) == 0\
                               else     tsr( ox, dt) if ist(ox[0], Integral) or ist(ox[0], Real)\
                               else bas.typ( ox)([toT(v, dt, ik) for v in ox])
    if      ist( ox,TYP[50]):return nmb.from_numpy(ox).to(dt) if dt is not None\
                               else nmb.FloatTensor(ox) if ox.dtype == nmp.float64\
                               else nmb.from_numpy(ox)
    if      ist( ox,TYP[10],
                    TYP[40]):return  ox # FIXME
    if      ist( ox,   'sc'):return  ox if fb\
                               else nmb.as_tensor(ox).to(dt) if dt is not NON\
                               else nmb.as_tensor(ox)
    raise TypeError("not support item type: {}".format(type(ox)))
def toT( *c,**g): return shftLar_Tsr( *c,**g)


shftLar_ = dict(
    n    = shftLar_Num
)
def shftLar( ox, fc='n'): return shftLar_[fc](ox)
def shftLas( ox, fc='n'): return ox.detach().cpu().numpy()

def shftLan( ox, fc='n'): return ox.detach().cpu().numpy()

'''
shft = dddd(dict(
   i = shftLai, # 畨
   r = shftLar, # 娄: 数
   s = shftLas, # 类: 類
   n = shftLan))# 粦: 亃\㔂\粼\斴\甐\䚏\翷
'''

def nPrm_ort(mod):
  pass
  
'''
nPrm_ = dict(
  otg = nPrm_ort,
  ran = nPrm_ran
)
'''

def    toD( ox: Any, dev: str, igk: list = []):
  if   ist( ox, nmb.nn.Module):
    return  ox.to(dev)
  elif ist( ox, nmb.Tensor):
    return  ox.to(dev)
  elif ist( ox, Sequence):
    if ist( ox, str):
      return  ox
    else:
      return [toD(t, dev) for t in  ox]
  elif ist( ox, dict):
    new_item = {}
    for k in  ox.keys():
      if k in igk:
        new_item[k] =  ox[k]
      else:
        new_item[k] = toD( ox[k], dev)
    return new_item
  elif ist( ox, Integral) or ist( ox, Real):
    return  ox
  elif ist( ox, nmp.ndarray) or ist( ox, nmp.bool_):
    return  ox
  elif  ox is None or ist( ox, str):
    return  ox
  else:
    raise TypeError("not support item type: {}".format(type( ox)))


# 包含数值的张量 [23A90] afc:.pop() -> .popleft()
def Tsr_Dix(tfc, afc=['stp']):
  ugd = tfc[afc[0]].unsqueeze(-1)
  #afc.popleft()
  if len(afc) > 1:
    for fc in afc[1:]:
      ugd = nmb.cat((ugd,tfc[fc].unsqueeze(-1)), -1)
  return ugd

def Tsr_Lix(tfc, afc=['stp']):
  ugd = tfc[afc[0]].unsqueeze(-1)
  #afc.popleft()
  if len(afc) > 1:
    for fc in afc[1:]:
      ugd = nmb.cat((ugd,tfc[fc].unsqueeze(-1)), -1)
  return ugd





def toL(item):

  if item is None:
    return item
  elif ist(item, nmb.Tensor):
    return item.tolist()
  elif ist(item, nmp.ndarray):
    return item.tolist()
  elif ist(item, list) or ist(item, tuple):
    return [toL(t) for t in item]
  elif ist(item, dict):
    return {k: toL(v) for k, v in item.items()}
  elif nmp.isscalar(item):
    return item
  else:
    raise TypeError("not support item type: {}".format(type(item)))

def tensor_to_list(item):
  if item is None:
    return item
  elif ist(item, nmb.Tensor):
    return item.tolist()
  elif ist(item, list) or ist(item, tuple):
    return [tensor_to_list(t) for t in item]
  elif ist(item, dict):
    return {k: tensor_to_list(v) for k, v in item.items()}
  elif nmp.isscalar(item):
    return item
  else:
    raise TypeError("not support item type: {}".format(type(item)))



def get_tensor_data(data: Any) -> Any:
  """
  Overview:
    Get pure tensor data from the given data(without disturbing grad computation graph)
  """
  if ist(data, nmb.Tensor):
    return data.data.clone()
  elif data is None:
    return None
  elif ist(data, Sequence):
    return [get_tensor_data(d) for d in data]
  elif ist(data, dict):
    return {k: get_tensor_data(v) for k, v in data.items()}
  else:
    raise TypeError("not support type in get_tensor_data: {}".format(type(data)))


def unsqueeze(data: Any, dim: int = 0) -> Any:
  if ist(data, nmb.Tensor):
    return data.unsqueeze(dim)
  elif ist(data, Sequence):
    return [unsqueeze(d) for d in data]
  elif ist(data, dict):
    return {k: unsqueeze(v, 0) for k, v in data.items()}
  else:
    raise TypeError("not support type in unsqueeze: {}".format(type(data)))


if  bas.Her(__name__):
    a = nmb.tensor([1.0, 1.0])
    b = shftLarTNum(a)
    print(b)