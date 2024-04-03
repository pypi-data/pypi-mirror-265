# 具有类型注释功能的ArgParse: ArgChecker
import sys
from typing import Any, Iterable, Optional, Union, overload
    
class ArgChecker:
    @staticmethod
    def __cast(v:str) -> 'Union[None,bool,int,float,str]':
        if v=="True": return True
        if v=="False": return False
        if v=="None": return None
        try:
            return int(v)
        except:
            pass
        try:
            return float(v)
        except:
            return v.strip('"')

    @staticmethod
    def get_dict(params:Union[str,Iterable[str]] = sys.argv[1:])->'dict[str,Union[str,Any]]':
        '''将输入参数以字典的形式返回'''
        if isinstance(params, str):
            params = params.split(sep=" ")
            new_params:list[str] = []
            in_quotes1 = False
            in_quotes2 = False
            current_param = ""
            for param in params:
                if param.startswith('"') and not param.endswith('"'):
                    in_quotes2 = True
                    current_param = param
                elif in_quotes2:
                    current_param += " " + param
                    if param.endswith('"'):
                        in_quotes2 = False
                        new_params.append('"'+current_param.strip('"')+'"')
                elif param.startswith("'") and not param.endswith("'"):
                    in_quotes1 = True
                    current_param = param
                elif in_quotes1:
                    current_param += " " + param
                    if param.endswith("'"):
                        in_quotes1 = False
                        new_params.append('"'+current_param.strip('"')+'"')
                else:
                    new_params.append(param)
            params = new_params
        
        cur_key = None
        ret:dict[str, Any] = {}
        for v in params:
            if v.startswith('-'):
                if cur_key != None:
                    ret[cur_key] = True
                cur_key = v.strip('-')
            elif cur_key != None:
                ret[cur_key] = ArgChecker.__cast(v)
                cur_key = None
            else:
                raise ValueError(f"无效参数'{v}'")
        if cur_key != None: ret[cur_key] = True
        return ret

    def __init__(self, pars:'Union[None,str,dict[str,Any]]' = None):
        if pars is None:
            self.__args = ArgChecker.get_dict()
        elif isinstance(pars, str):
            self.__args = ArgChecker.get_dict(pars)
        elif isinstance(pars, dict):
            self.__args = pars
        else:
            raise TypeError("参数类型错误")
    
    def pop_bool(self, key:str) -> bool:
        if self.__args.pop(key, False): return True
        return False
    
    def pop_int(self, key:str, default:Optional[int] = None) -> int:
        val = self.__args.pop(key, default)
        if val is None: raise ValueError(f"必须指定'{key}'参数")
        return int(val)
    
    def pop_str(self, key:str, default:Optional[str] = None) -> str:
        val = self.__args.pop(key, default)
        if val is None: raise ValueError(f"必须指定'{key}'参数")
        return str(val).strip('"')
   
    def pop_float(self, key:str, default:Optional[float] = None) -> float:
        val = self.__args.pop(key, default)
        if val is None: raise ValueError(f"必须指定'{key}'参数")
        return float(val)
    
    def empty(self) -> bool:
        return len(self.__args) == 0
    
    def keys(self): return self.__args.keys()
    def values(self): return self.__args.values()
    def items(self): return self.__args.items()

    def __str__(self):
        return str(self.__args)