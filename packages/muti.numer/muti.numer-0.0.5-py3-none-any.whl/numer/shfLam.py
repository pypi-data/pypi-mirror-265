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
_LC_TAN = ['train','drop','tre',TYP[60].train]
_LC_RAN = ['tests','eval','vlu',TYP[60].eval ]
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
  non   = None
)
def LaiRMod(mod, fc, mm='cuda',_fb=False):
    print(f"[{_JC_NYM} | mod] : load {mod._jc} by { fc}")
    if fc in _LC3REV: pass# nPrm_[ fc](mod)
    else:
      _lc = bas.getPath(fc)
      _mm = mm if len(mm) <= 4 else mm[:4] 
      loadMod(mod,_lc,_mm)

def LaiPMod( ox:TYP[60], fc, fb=TRU):
    if fb :  ox= ox.state_dict() # 只存其参
    if fc[:3]in _LC3PEV:
            _lc=bas.getPath(fc[:3]) + fc[3:] # FIXME
    else  : _lc=bas.getPath( fc, TRU) # os.makedirs(os.path.dirname(_fc))
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

def fmrtDmm( fx):
    _fh_Dmm= fx if ist( fx,TYP[42]) else shftLanDdic(fx)
    if _fh_Dmm['t'] == 'm': return _fh_Dmm
    _fh_Dmm.setdefault(_KY_[0],nmb.float32) 
    _fh_Dmm.setdefault(_KY_[1],nmb.device('cuda' if nmb.cuda.is_available() else 'cpu')) 
    return _fh_Dmm

def shftLai( ox, fh): return ox.to(**fmrtDmm(fh))

def shftLarTNum( ox:nmb.Tensor): return ox.detach().cpu().numpy()
#def shftLar_num(ox): return ox.detach().cpu().numpy()
def shftLar_Num( ox:Any, fh={'t':NON}):
    # FIXME
    if   ox is  NON: return NON
    _fc_typ= fh['t']
    if      ist( ox,TYP[30]): return shftLarTNum(ox).astype(_fc_typ) if _fc_typ else shftLarTNum(ox)
    if      ist( ox,TYP[20]): return ox.astype(_fc_typ)  if _fc_typ else ox
    if      ist( ox,TYP[10]): return ox
    # namedtuple
    if  hasattr( ox,'_fields'):        return type(ox)(*[shftLar_Num(ex, fh) for ex in ox])
    if      ist( ox,TYP[14],TYP[41]):  return None if  len( ox) == 0 else [shftLar_Num(ex, fh) for ex in ox]
    if      ist( ox,TYP[42]):          return {k:shftLar_Num(ex, fh) for k, ex in ox.items()}
    if nmp.isscalar(ox):               return nmp.array(ox)
    raise TypeError("not support item type: {}".format(type(ox)))

def toN( *c,**g): return shftLar_Num( *c,**g)

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

def    toD( ox: Any, device: str, ignore_keys: list = []):
  if   ist( ox, nmb.nn.Module):
    return  ox.to(device)
  elif ist( ox, nmb.Tensor):
    return  ox.to(device)
  elif ist( ox, Sequence):
    if ist( ox, str):
      return  ox
    else:
      return [toD(t, device) for t in  ox]
  elif ist( ox, dict):
    new_item = {}
    for k in  ox.keys():
      if k in ignore_keys:
        new_item[k] =  ox[k]
      else:
        new_item[k] = toD( ox[k], device)
    return new_item
  elif ist( ox, Integral) or ist( ox, Real):
    return  ox
  elif ist( ox, nmp.ndarray) or ist( ox, nmp.bool_):
    return  ox
  elif  ox is None or ist( ox, str):
    return  ox
  else:
    raise TypeError("not support item type: {}".format(type( ox)))

def to_tensor(
    item: Any,
    dtype: Optional[nmb.dtype] = None,
    ignore_keys: list = [],
    transform_scalar: bool = True
):
  r"""
  Overview:
    Change `numpy.ndarray`, sequence of scalars to nmb.Tensor, and keep other data types unchanged.
  Arguments:
    - item (:obj:`Any`): the item to be changed
    - dtype (:obj:`type`): the type of wanted tensor
  Returns:
    - item (:obj:`nmb.Tensor`): the change tensor

  .. note:

    Now supports item type: :obj:`dict`, :obj:`list`, :obj:`tuple` and :obj:`None`
  """

  def transform(d):
    if dtype is None:
      return nmb.as_tensor(d)
    else:
      return nmb.tensor(d, dtype=dtype)

  if ist(item, dict):
    new_data = {}
    for k, v in item.items():
      if k in ignore_keys:
        new_data[k] = v
      else:
        new_data[k] = to_tensor(v, dtype, ignore_keys, transform_scalar)
    return new_data
  elif ist(item, list) or ist(item, tuple):
    if len(item) == 0:
      return []
    elif ist(item[0], Integral) or ist(item[0], Real):
      return transform(item)
    elif hasattr(item, '_fields'):  # namedtuple
      return type(item)(*[to_tensor(t, dtype) for t in item])
    else:
      new_data = []
      for t in item:
        new_data.append(to_tensor(t, dtype, ignore_keys, transform_scalar))
      return new_data
  elif ist(item, nmp.ndarray):
    if dtype is None:
      if item.dtype == nmp.float64:
        return nmb.FloatTensor(item)
      else:
        return nmb.from_numpy(item)
    else:
      return nmb.from_numpy(item).to(dtype)
  elif ist(item, bool) or ist(item, str):
    return item
  elif nmp.isscalar(item):
    if transform_scalar:
      if dtype is None:
        return nmb.as_tensor(item)
      else:
        return nmb.as_tensor(item).to(dtype)
    else:
      return item
  elif item is None:
    return None
  elif ist(item, nmb.Tensor):
    if dtype is None:
      return item
    else:
      return item.to(dtype)
  else:
    raise TypeError("not support item type: {}".format(type(item)))

def to_list(item):

  r"""
  Overview:
    Transform `nmb.Tensor`, `numpy.ndarray` to `list`, keep other data types unchanged
  Arguments:
    - item (:obj:`Any`): the item to be transformed
  Returns:
    - item (:obj:`list`): the list after transformation
  .. note::
    Now supports item type: :obj:`nmb.Tensor`, :obj:`numpy.ndarray`, :obj:`dict`, :obj:`list`, \
    :obj:`tuple` and :obj:`None`
  """

  if item is None:
    return item
  elif ist(item, nmb.Tensor):
    return item.tolist()
  elif ist(item, nmp.ndarray):
    return item.tolist()
  elif ist(item, list) or ist(item, tuple):
    return [to_list(t) for t in item]
  elif ist(item, dict):
    return {k: to_list(v) for k, v in item.items()}
  elif nmp.isscalar(item):
    return item
  else:
    raise TypeError("not support item type: {}".format(type(item)))


def tensor_to_list(item):
  r"""
  Overview:
    Transform `nmb.Tensor` to `list`, keep other data types unchanged
  Arguments:
    - item (:obj:`Any`): the item to be transformed
  Returns:
    - item (:obj:`list`): the list after transformation

  .. note::

    Now supports item type: :obj:`nmb.Tensor`, :obj:`dict`, :obj:`list`, :obj:`tuple` and :obj:`None`
  """
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


def same_shape(data: list):
  r"""
  Overview:
    Judge whether all data elements in a list have the same shape.
  Arguments:
    - data (:obj:`list`): the list of data
  Returns:
    - same (:obj:`bool`): whether the list of data all have the same shape
  """
  assert (ist(data, list))
  shapes = [t.shape for t in data]
  return len(set(shapes)) == 1


class LogDict(dict):
  '''
  Overview:
    Derived from ``dict``; Would transform ``nmb.Tensor`` to ``list`` for convenient logging.
  '''

  def _transform(self, data):
    if ist(data, nmb.Tensor):
      new_data = data.tolist()
    else:
      new_data = data
    return new_data

  def __setitem__(self, key, value):
    new_value = self._transform(value)
    super().__setitem__(key, new_value)

  def update(self, data):
    for k, v in data.items():
      self.__setitem__(k, v)


def build_log_buffer():
  r"""
  Overview:
    Builg log buffer, a subclass of dict, which can transform the input data into log format.
  Returns:
    - log_buffer (:obj:`LogDict`): Log buffer dict
  """
  return LogDict()




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

# [23A90] afc:.pop() -> .popleft()
def rTsr(tfc, afc=['stp']):
  ugd = tfc[afc[0]].unsqueeze(-1)
  #afc.popleft()
  if len(afc) > 1:
    for fc in afc[1:]:
      ugd = nmb.cat((ugd,tfc[fc].unsqueeze(-1)), -1)
  return ugd

if  bas.Her(__name__):
    a = nmb.tensor([1.0, 1.0])
    b = shftLarTNum(a)
    print(b)