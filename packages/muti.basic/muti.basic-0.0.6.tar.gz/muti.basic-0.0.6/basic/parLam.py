"""
 #  bas-muti :: par-lam 析函集
 @  E.C.Ares
 !  MIT DIVIƷON
 `  Lam of part builtin basic-python
"""
# r(import-refs)
#       r.. im
from   .depLam       import *
import argparse as arg
import json
import yaml  # ruamel.yaml pyyaml
import importlib.util as pyth
# s
_JC_NYM = 'lam_par'


partArp = dict(
     j  = json.loads,
     y  = yaml.safe_load
)
def partArg( fh, zc, fb_las=False):
    _or_par  = arg.ArgumentParser(description=zc)
    for _li in  range(  len( fh)):
        _fh_cfg  =   fh[_li]
        if not _fh_cfg[2]: _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1])
        elif isinstance(_fh_cfg[2], list):
            if   len(_fh_cfg[2]) == 1: _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], action = 'store_'+_fh_cfg[2][0])
            elif len(_fh_cfg[2]) == 2 and _fh_cfg[2][1] in ['+',',']:
                _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], type = _fh_cfg[2][0], nargs=_fh_cfg[2][1])
            else:
                _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], choices = _fh_cfg[2])
        else:    # elif afc_cfg_tmp[1] is class (else: choices)
            _or_par.add_argument(_fh_cfg[0], default = _fh_cfg[1], type = _fh_cfg[2])
    if fb_las: return  _or_par.parse_args()
    return  _or_par.parse_args().__dict__



# json
def Imp_Cfp( lc, fc, fg={'f':'r','c':'utf-8'}):
    _fc  =   fc[ 0]
    #_fb  = True if len(fc) == 2 else False 
    return  partArp[_fc](open( lc, fg['f'], encoding=fg['c']).read()) # read_text()

# 必须是 .py 结尾
def Imp_Cfg( lc, *c,**g):
    _jc = os.path.basename( lc)
    #_lc = os.path.dirname(  lc)
    # 创建模块规范
    spe = pyth.spec_from_file_location(_jc[:-4], lc)
    # 从规范加载模块
    cfg = pyth.module_from_spec(spe)
    # 执行模块中的代码
    spe.loader.exec_module(cfg)
    if hasattr(cfg, 'getrArg'): return partArg(cfg.getrArg(), *c,**g)
    else: raise NotImplementedError
    
#  a = Imp_Arg,
Imp_ = dict(
   p = Imp_Cfg,
   j = Imp_Cfp,
   y = Imp_Cfp)

def Imp( lc, fc, *c,**g):
    #if lc[1] not in [':','h']:
    return Imp_[fc](lc, fc, *c,**g)

_LC_HER = os.getcwd()

_JC_TOK_={
    'r' :['rut','root','/','\\'],
    'a' :['aut','ares','~','D:'],
    'b' :['but','base','_','..'],
    'c' :['cut','cwdb','.','__']}

_LC_RUT = os.path.abspath(os.sep)
_LC_HOM = os.path.expanduser("~")
# 得到合法的 lc/jc 路径, 若 fb 且 lc不存在 则创建
def Pth( jc, lc=NON, fb=TRU) :
    _lc                              =  os.path.dirname(             jc) # '' 或 jc前缀
    _jc                              =  os.path.basename(            jc)
    if  ist( lc,NON):           _lc  =  os.path.abspath(            _lc)\
                                    if  os.path.isdir(              _lc)\
                                   else os.path.join(os.getcwd(),   _lc)
    elif lc  in _JC_TOK_['r']:  _lc  =  os.path.join(_LC_RUT    ,   _lc)
    elif lc  in _JC_TOK_['a']:  _lc  =  os.path.join(_LC_HOM    ,   _lc)
    elif lc  in _JC_TOK_['b']:  _lc  =  os.path.join(os.getcwd(),   _lc) 
    elif lc  in _JC_TOK_['c']:  _lc  =  os.path.join(os.getcwd(),   _lc) #os.getcwdb()
    else:                       _lc  =  os.path.join(os.path.abspath(lc),_lc)
    if fb and not os.path.isdir(_lc) :  os.makedirs( _lc)
    return        os.path.join( _lc,_jc)