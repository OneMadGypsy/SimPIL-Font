from PIL       import ImageFont
from glob      import iglob
from functools import partial
import json, copy, platform


def __fontlib(fontmap:dict, family:str='', fontdir:str='', dumpmap:bool=False) -> dict|set:
    if fontdir or (not fontmap) or (not family):
        fontdir = fontdir or FONTDIR
        for fn in iglob(fr'{fontdir}**/*.ttf', recursive=True):
            try:
                ttf = ImageFont.truetype(font=fn)
            except: ...
            else:
                name, face          = ttf.getname() 
                face                = face.lower()
                fontmap[name]       = fontmap.get(name, {})
                fontmap[name][face] = fn
        
    if dumpmap:
        with open('fonts.json', 'w') as f:
            f.write(json.dumps(fontmap, indent=4))
            
    return copy.deepcopy(fontmap.get(family, {}))
    
    
FONTDIR = {
    "Windows": "c:/Windows/Fonts/",
    #"Darwin" : "",
    #"Linux"  : ""
}.get(platform.system(), '')

#singleton-------------------v
FONTMAP = partial(__fontlib, {})
FONTMAP(fontdir=FONTDIR)


class SimPILFont:
    #https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
    ENCODINGS = "unic", "symb", "DOB", "ADBE", "ADBC", "armn", "sjis", "gb", "big5", "ans", "joha", "lat1"

    ## STATIC

    #whichever one exists first:
    #  the face you requested else "regular" else the first face in keys
    @staticmethod
    def bestface(face:str, faces:dict) -> str:
        dflt = 'regular'
        if faces and (keys := faces.keys()): 
            if not dflt in keys:
                dflt = next(fc for fc in keys)
            if not face in keys:
                face = dflt
        else:
            face = ''
                
        return face
        
    #parse font string and return parts
    @staticmethod      
    def metadata(font:str) -> tuple:
        font = font.replace('{','').replace('}','') #for tk style font str
        fmly, face, size = [], [], 0
        
        for part in font.split(' '):
            if part.isdigit(): size = int(part)
            else             : (face, fmly)[part != part.lower()].append(part)
                
        family = ' '.join(fmly)
        face   = ' '.join(face)
        
        return family, face, size
    
    #get an ImageFont without a Font instance
    #partial font requests are not supported
    @staticmethod  
    def instance(font:str, encoding:str='unic') -> ImageFont.FreeTypeFont:
        family, face, size = SimPILFont.metadata(font)
        
        encoding = encoding if encoding in ENCODINGS else 'unic'
        faces    = FONTMAP(family)
        face     = SimPILFont.bestface(face, faces)
        path     = faces.get(face, '')
        
        return ImageFont.truetype(path, size or 12, encoding=encoding)
        
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
    def path(self) -> str|None:
        return self._path
        
    @property
    def font(self) -> ImageFont.FreeTypeFont:
        return self._font
        
    @property
    def encoding(self) -> str:
        return self._encoding
        
    @encoding.setter
    def encoding(self, enc:str) -> None:
        self._encoding = enc if enc in SimPILFont.ENCODINGS else 'unic'
        
    #allow partial font requests
    #ex:
    #    ttf      = Font('Verdana 16 bold italic')
    #    ttf.font = '18'            # -> "Verdana 18 bold italic"
    #    ttf.font = '22 regular'    # -> "Verdana 22 regular"
    #    ttf.font = 'Consolas bold' # -> "Consolas 22 bold"
    @font.setter
    def font(self, font:str) -> None:
        family, face, size = SimPILFont.metadata(font)
        
        self._family = family or getattr(self, '_family', 'Arial')
        self._size   = size   or getattr(self, '_size'  , 12)
        self._faces  = FONTMAP(self._family)
        self._face   = SimPILFont.bestface(face or getattr(self, '_face', ''), self._faces)
        self._path   = self._faces.get(self._face, '')
        self._font   = ImageFont.truetype(self._path, self._size, encoding=self._encoding)
        
    ## DUNDER

    def __init__(self, font:str, encoding='unic'):
       self.encoding = encoding
       self.font     = font
       
    def __str__(self) -> str:
        return ' '.join((self._family, f'{self._size}', self._face))
        
    def __repr__(self) -> str:
        return str(self)
        
    ## PUBLIC METHODS
       
    def bbox(self, text:str) -> tuple:
        return self.font.getbbox(text)
        
    def offset(self, text:str) -> tuple:
        return self.font.getoffset(text)
