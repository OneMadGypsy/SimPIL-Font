import json, shelve, os, zipfile as zf
from   dataclasses import dataclass, KW_ONLY, InitVar, field, asdict
from   typing      import Iterable, Any, Iterator

#app directory
CWD     = os.getcwd()

#directories
HOMEDIR = os.path.join(CWD, 'dat')
if not os.path.isdir(HOMEDIR): os.mkdir(HOMEDIR)

FONTDIR = os.path.join(HOMEDIR, 'fonts')
if not os.path.isdir(FONTDIR): os.mkdir(FONTDIR)



@dataclass
class DBEntry_t:
    id    :str
    type  :str = 'all'

    @property 
    def asdict(self) -> dict:
        return asdict(self)
        
    def __repr__(self) -> str:
        return str(self)
        
    def __str__(self) -> str:
        return json.dumps(self.asdict, indent=4)
        
    def __call__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            try   : getattr(self, key)
            except: ...
            else  : setattr(self, key, value)
        

class DB:
    def __init__(self, dbname='generic'):
        self._db          = os.path.join(HOMEDIR, dbname).replace('\\','/')
        self._jzon        = f'{self._db}.jzon' #zipped json
        self.__registered = dict()
        
    #entire database as "pretty-printed" json string
    def __repr__(self) -> str:
        return str(self)
        
    #entire database as "pretty-printed" json string
    def __str__(self) -> str:
        out = '{}'
        with shelve.open(self._db) as db:
            out = json.dumps(dict(db), indent=4)
        return out
        
    def __getitem__(self, eid:str) -> dict|Iterable|DBEntry_t:
        entry = {}
        
        with shelve.open(self._db) as db:
            entry = db.get(eid, {})
                
        if T := self.__registered.get(entry.get('type', '')):
            entry = T(**entry)
            
        return entry
        
    def __setitem__(self, eid:str, entry:dict|Iterable|DBEntry_t) -> None:
        if isinstance(entry, DBEntry_t):
            entry  = entry.asdict
            
        with shelve.open(self._db) as db:
            db[eid] = entry
            
    #registering types returns a type instance, instead of a dict, for all methods that return database entries
    def register_type(self, enttype:str, entity:DBEntry_t):
        self.__registered[enttype] = entity
            
    # PROXY        
            
    #get database keys of .type
    def keys(self, enttype:str|None=None) -> list:
        with shelve.open(self._db) as db:
             enttype = enttype or 'all'
             return list(filter(lambda e: enttype in ('all', db[e].get('type')), db.keys()))
      
    #get database values as type of .type
    def values(self, enttype:str|None=None, cast:bool=True) -> list:
        out     = []
        enttype = enttype or 'all'
        T       = False if not cast else self.__registered.get(enttype)
        
        with shelve.open(self.db) as db:
             for entry in db.values():
                if enttype in ('all', entry.get('type')):
                    if T: entry = T(**entry)
                    out.append(entry)
                    
        return out
      
    #get database items as type of .type
    def items(self, enttype:str|None=None, cast:bool=True) -> Iterator:
        enttype = enttype or 'all'
        T       = False if not cast else self.__registered.get(enttype)
        
        with shelve.open(self._db) as db:
            for eid, entry in db.items():
                if enttype in ('all', entry.get('type')):
                    if T: entry = T(**entry)
                    yield eid, entry
    
    #overwrite the database with an empty one (flag='n')
    def clear(self) -> None:
        with shelve.open(self._db, flag='n'):
            ...  
    
    # TRANSFORMERS
        
    #database to dictionary
    def todict(self, enttype:str|None=None) -> dict:
        return {k:v for k,v in self.items(enttype or 'all', False)}
        
    #include `data` in the database  
    def dict2db(self, data:dict|DBEntry_t, overwrite:bool=False) -> None:
        if not isinstance(data, dict):
            raise ValueError('data must be a dict of entries')
        
        flag = ('c','n')[overwrite]
        with shelve.open(self._db, flag=flag) as db:
            for eid, entry in data.items():
                if isinstance(entry, DBEntry_t):
                    entry = entry.asdict
                db[eid] = entry
                
    #dump database to jzon file  
    def db2jzon(self) -> None:
        with zf.ZipFile(self._jzon, mode='w', compression=zf.ZIP_LZMA) as zip:
            zip.writestr('database.json', f'{self}')
         
    #load database from jzon file         
    def jzon2db(self) -> None:
        if not os.path.isfile(self._jzon): return
        with zf.ZipFile(self._jzon, mode='r') as zip:
            with zip.open('database.json') as file:
                self.dict2db(json.load(file), True)
            
    # GET/DEL KEY(S)
       
    def get_keys(self, keys:Iterable, eid:str) -> Any:
        out = None
        
        if entry := self[eid]:
            if isinstance(keys, list|tuple):
                out = {key:entry.get(key) for key in keys}
            else: 
                out = entry.get(keys)
                     
        return out
    
    def delete_keys(self, keys:list|str, eid:str) -> None:
        keys = keys if isinstance(keys, list|tuple) else (keys, )
        if entry := self[eid]:
            for key in keys: del entry[key]
            self[eid] = entry 
                
    # GET/DEL ENTRIES
             
    def entries(self, eids:Iterable, enttype:str|None=None, cast:bool=True) -> list:
        out = []
        eids    = eids if isinstance(eids, list|tuple) else (eids,)
        enttype = enttype or 'all'
        T       = False if not cast else self.__registered.get(enttype)
        
        with shelve.open(self._db) as db:
            for eid in eids:
                if entry := db.get(eid, {}):
                    if enttype in ('all', entry.get('type')):
                        if T: entry = T(**entry)
                        out.append(entry)
                    
        return out
               
    #delete 1 or more database entries by id
    def delete(self, eids:Iterable) -> None:
        eids = eids if isinstance(eids, list|tuple) else (eids,)
        with shelve.open(self._db) as db:
            for eid in eids:
                if db.get(eid): del db[eid]
            
            
#



