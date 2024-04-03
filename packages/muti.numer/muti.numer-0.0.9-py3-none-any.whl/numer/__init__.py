_JC_NYM = "muti.torch"
import os

_fc  =  os.getenv( 'FC_IMP')
if _fc is NON or _fc== '': _fc='tn'
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

# core.numer
from .depLam import *
# 形式转换: mod\dat 放置到 MEM\CPU\GPU\.. ; .tensor .ndarrray 等类转换
from .iniLam import *
# 更新 pln or BW\OPT| loss.backward() 网络反向传播, 优化器更新
from .shfLam import *
# 初化 for model\optimizer : Model(arg_model)\Optimizer(arg_opt, model.parameters())
#from .updLam import *
# 算路              | y = mod.forward(x) : mod = ModLas(cfg)
from .modLas import *
# 特函 esp.Los·拉形 | los(y, y')         : los = LosLam(cfg) 
#from .conLam import *