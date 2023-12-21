from __future__  import annotations
from  .db          import *
from   glob        import iglob
from   typing      import Iterable, Any
from   functools   import partial
from   dataclasses import dataclass, field, asdict, InitVar, KW_ONLY
from   PIL         import ImageFont
import os, re

""" ENTRY TYPES
"""

@dataclass
class Font_t(DBEntry_t):
    type    :str  = 'font'
    options :list = field(default_factory=list)
    faces   :dict = field(default_factory=dict)
    

@dataclass
class FontPath_t(DBEntry_t):
    type    :str = 'fontpath'
    modified:int = 0


SLASH = partial(re.compile(r'\\+').sub, '/')


""" FONT DATABASE
"""
class FontDatabase(DB):
    def __init__(self, dbname='fonts'):
        DB.__init__(self, dbname)
        
        #these types will be returned as their type, instead of dict, for all methods that return a database entry
        self.register_type(Font_t.type    , Font_t    )
        self.register_type(FontPath_t.type, FontPath_t)
        
    def add_fonts(self, path:str) -> None:
        path = SLASH(path)
        
        #trailing slash is required
        if path[-1] != '/': path = f'{path}/'
        
        #get folder modified time for comparison
        mod = os.path.getmtime(path)
        
        #determine if we need to update/create an entry
        for key in self.keys(FontPath_t.type):
            #the user may try to request a subdirectory of a directory we already gathered
            if key in path:
                #force path to root path, if applicable
                path = key
                
                #if nothing has changed since the last update ~ get out of here
                if self[key].modified >= mod:
                    return
        else: 
            #path either does not exist or needs an update overwrite
            self[path] = FontPath_t(path, modified=mod)
            
        print('Gathering Fonts')
                
        fontmap = dict() 
        
        #traverse directory, storing metadata for ttf fonts
        for fn in iglob(fr'{path}**/*.ttf', recursive=True):
            fn = SLASH(os.path.abspath(fn))
            try:
                ttf = ImageFont.truetype(font=fn)
            except: ...
            else:
                family, face    = ttf.getname() 
                face            = face.lower()
                
                fontmap[family] = fontmap.get(family, Font_t(family))
                fontmap[family].faces[face.replace(' ', '')] = fn
                fontmap[family].options.append(face)
                
        print('Updating Font Database - this may take several seconds.')
        
        #commit to database
        self.dict2db(fontmap)
       
       
""" FONT
"""
class Font:
    #https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
    ENCODINGS = "unic", "symb", "DOB", "ADBE", "ADBC", "armn", "sjis", "gb", "big5", "ans", "joha", "lat1"

    ## STATIC

    @staticmethod
    def bestface(face:str, options:tuple) -> str:
        face = face.replace(' ', '')
        
        for dflt in ('regular', 'book'):
            if dflt in options: break
        else: dflt = options[0]
        
        if options: 
            if not face in options:
                face = dflt
        else: face = ''
                
        return face
        
    @staticmethod      
    def metadata(font:str) -> tuple:
        fmly, face, size = [], [], 0
        
        for part in font.split(' '):
            if part.isdigit(): size = int(part)
            else             : (face, fmly)[part != part.lower()].append(part)
                
        return ' '.join(fmly), ' '.join(face), size
    
    ## PROPERTIES

    @property
    def family(self) -> str:
        return self._family
        
    @property
    def face(self) -> str:
        return self._face
        
    @property
    def size(self) -> int:
        return self._size
        
    @property
    def path(self) -> str:
        return self._path
       
    @property
    def faces(self) -> dict:
        return self._db[self._family].faces
        
    @property
    def options(self) -> tuple:
        return tuple(self._db[self._family].options)
        
    @property
    def encoding(self) -> str:
        return self._encoding
        
    @encoding.setter
    def encoding(self, enc:str) -> None:
        self._encoding = enc if enc in Font.ENCODINGS else 'unic'
            
    @property
    def font(self) -> ImageFont.FreeTypeFont:
        return self._font
        
    @font.setter
    def font(self, font:str) -> None:
        if not font: return #falsy call, ignore and move on
        
        #get details
        family, face, size = Font.metadata(font)
        
        #use detail else nochange else default
        self._family  = family or getattr(self, '_family', 'Arial')
        self._size    = size   or getattr(self, '_size'  , 12)
        self._face    = face   or getattr(self, '_face'  , '')
        
        #find the database entry for this family
        if not (entry := self._db[self._family]):
            raise ValueError('Unknown Family')
            
        #prepare path
        faces      = entry.faces
        face       = Font.bestface(self._face, tuple(faces))
        self._path = faces.get(face, '') #it's impossible for the face not to exist
        
        #adjust self._face for "best face"
        for option in entry.options:
            if option.replace(' ', '') == face:
                self._face = option
                break

        #final ImageFont instance
        self._font = ImageFont.truetype(self._path, self._size, encoding=self._encoding)
        
    @property  #return tuple of "known" font directories
    def fontdirs(self) -> tuple:
        return tuple(self._db.todict(FontPath_t.type).keys())
    
    @fontdirs.setter  #store font data from 1 or more directories, including subdirectories
    def fontdirs(self, paths:Iterable) -> None:
        if not paths: return
        
        #combine `paths` arguments into one list
        j, paths = [], (paths if isinstance(paths, list|tuple) else (paths, ))
        func     = j.append, j.extend
        for item in paths:
            func[isinstance(item, tuple|list)](item)
            
        #format paths, drop duplicate paths, process paths
        for path in set(map(SLASH, j)):
            self._db.add_fonts(path)
        
    ## DUNDER

    def __init__(self, font:str|None=None, fontdirs:Iterable='', encoding:str='unic') -> None:
        #database instance
        self._db      = FontDatabase()
        #establish encoding
        self.encoding = encoding
        #check/include all possible font directories - duplicates are dropped
        self.fontdirs = FONTDIR, self.fontdirs, fontdirs
        #instance ImageFont font
        self.font     = font
     
    def __str__(self) -> str:
        return ' '.join((self._family, f'{self._size}', self._face))
        
    def __repr__(self) -> str:
        return str(self)
        
    #inline font set
    def __call__(self, font:str) -> Font:
        self.font = font
        return self
    
    ## PROXIES
       
    #basic bbox
    def bbox(self, text:str) -> tuple:
        return self.font.getbbox(text)
    
    #smallest possible bbox
    def min_bbox(self, text:str) -> tuple:
        x, y, w, h = self.font.getbbox(text)
        return -x, -y, w-x, h-y
        
    #(right/bottom) margins mirror the (left/top) margins, respectively
    def max_bbox(self, text:str) -> tuple:
        x, y, w, h = self.font.getbbox(text)
        return 0, 0, w+x, h+y
        
    #this is suspiciously always the same as `.bbox(text)[0:2]`
    def offset(self, text:str) -> tuple:
        return self.font.getoffset(text)
    
        
#



