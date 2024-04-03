# 
from   argparse import Namespace as Nym
import   torch                  as nmb
from                  .iniLam import *
from                  .shfLam import *



class   UMA(nmm.Module):
    def __init__(self, cfx):
        super().__init__()
        self.setnPar(cfx)    # 参数解析
        self.initUti()       # 母工具
        self.initCas()       # 结构初始化
        self.initCat()       # 系数初始化
    
    # 解析设置类内变量  
    def setnPar(self, cfx):
        self._qiOsiz = cfx.qLsiz[0]
        self.nmm_ini_= bas.Dic(
                 bia = lambda bias: getrNPI(cfx.jTnym['nbi'])(bias, 0),
                 wei = lambda weit: getrNPI(cfx.jTnym['nwi'])(weit, gain=rGai_fnn({'nym':cfx.jTnym['nla']}))    # self.nmm_npi
        )
    # 初始化结构
    def initCas(self):
        pass
        #os.environ["CUDA_VISIBLE_DEVICES"] = "3,2,0,1"
        self._module = nmm.DataParallel(self._module, device_ids=[0,2,3]).cuda()
    def initUti(self):
        self.ini_ = lambda mod: initMod(mod, self.nmm_ini_)
        self.seq_ = nmm.Sequential
    # 初始化参数
    def initCat(self):
        pass

    def addnMod(self, mod, nym): return self.add_module(nym, mod)
    def getrWrd(self,*i)       : return self.forward(*i)
    def set_dmm(self,mm)       : shftLai(self, mm) # gpu cpu ipu cuda 123 empty sbe called before constructing optimizer
    def set_rmm(self,nm='tre') : Lam_mod(self.module(), nm) # test, train(mode), eval, run
    def getrPat(self, rec=True): return self.parameters(recurse=rec) # self.get_parameter()
    def detrMod(self)          :
        for child in self.children(): yield child
    def getrChi(self)          :
        for child in self.children(): yield child