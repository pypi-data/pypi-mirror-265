"""
 #  bas-muti :: typ-las 型类集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Las of type builtin basic-python
"""
# r
from depLam import *
from abc    import ABC,\
                   abstractmethod as _am
from copy   import copy           as _cp,\
                   deepcopy       as dcp
# s
#_L  =  TYP[14]([TYP[41],TYP[14]])
_L   =  TYP[41],TYP[14]
_D   =  TYP[42]
# t
typ  =lambda x  : type(x)

cp_  = dict(
  _  = _cp,
  l  = lcp,
  d  = dcp
)

class   Di_(ABC):
    def __init__(      self, *c,**g):
        #self._JC  =   self.ic_(   )
        self.upd_cfg(**self.frm( *c))
        self.upd_cfg(           **g)
    # ittr
    def is_(self): return self.__class__
    def ic_(self): return self.is_().__name__

    def frm(self, *c): return c[0] if c and ist(c[0],_D) else {}
    # 增量更新
    def upd(    self,ox:_D, fc='l'):
        _ox=cp_[fc]( ox)
        self.update(_ox)
    # g is dict
    def upd_cfg(self,  **g):
        if    g:self.upd(g)
    @_am
    def update(self, ox: _D, *c): raise NotImplementedError

# dims
class   Dim(Di_, Namespace):
    #for _jc in  ox:  setattr(self, _jc, ox[_jc])
    def update(self, ox): setnDic(self,ox)

# dict
class   Dic(Di_, dict):
    def update(self, ox): super(Di_,self).update(ox)
    
# dixt
class   Dix(Dic):
    
    #def __init__( self, *c,**g): super.__init__(self, *c,**g)
    def __setattr__(   self, jc, ox):
        _ZS = self.__class__ # 方法可继承
        # FIXME SET\OTH FORMAT
        if      ist(ox,*_L):    _ox = typ(ox)(_ZS(_ex) if ist(_ex, _D) else _ex for _ex in ox)
        elif    ist(ox, _D):    _ox = _ZS(ox)
        else               :    _ox =     ox
        super().__setattr__( jc,_ox)
        super().__setitem__( jc,_ox)
    __setitem__=__setattr__

    # FIXME set_attr 暂时不管 copy
    def upd(    self,ox:_D,*arg):
        self.update( ox)
    #for    _jc  in  ox : setattr(self,   _jc, ox[_jc]) 
    def update(self, ox): setnDic(self,ox)
    # poptItm
    def pop(self, k, *c):
        if self.__hasattr__(k): self.__delattr__(k)
        return   super().pop(k, *c)

if Her(__name__): h = Dic(ox=1, c=1)