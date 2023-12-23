from __future__ import annotations
from   glob    import iglob
from   typing  import Iterable
from   PIL     import ImageFont
import os

class SimPILFont:
    # https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
    ENCODINGS = "unic", "symb", "DOB", "ADBE", "ADBC", "armn", "sjis", "gb", "big5", "ans", "joha", "lat1"
        
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
        
    @property # supported faces for the current font 
    def facetypes(self) -> tuple: 
        return tuple(self._facetypes)
           
    @property
    def font(self) -> ImageFont.FreeTypeFont: 
        return self._font
        
    def __init__(self, fontdirs:Iterable) -> None:
        self._fontdirs = fontdirs if isinstance(fontdirs, list|tuple) else (fontdirs, )
        
    def __str__(self) -> str:
        return ' '.join((self._family, f'{self._size}', self._face))
        
    def __call__(self, font:str, encoding:str='unic') -> SimPILFont:
        encoding = encoding if encoding in SimPILFont.ENCODINGS else 'unic'
        
        # get details
        family, face, size = [], [], 0
        
        for part in font.split(' '):
            if part.isdigit(): size = int(part)
            else: 
                lower = part.lower()
                (face, family)[part != lower].append(part)
                
        family, face = ' '.join(family), ' '.join(face)
        
        # use detail else nochange else default
        self._family    = family or getattr(self, '_family', 'Arial'  )
        self._size      = size   or getattr(self, '_size'  , 12       )
        self._face      = face   or getattr(self, '_face'  , 'regular')
        self._facetypes = []
        
        faces = dict()
        found = False
        fam   = self._family.lower().replace(' ', '')
        
        # find font via family and face
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/*.ttf', recursive=True):
                fn = os.path.abspath(fn)
                
                try   : ttf = ImageFont.truetype(font=fn)
                except: ...
                else  :
                    family, face = ttf.getname() 
                    
                    if fam == family.lower().replace(' ', ''):
                        found = True
                        face  = face.lower()
                        self._facetypes.append(face)
                        faces[face.replace(' ', '')] = fn
                    elif found: break
                    
            if found: break
        else: 
            raise ValueError('No font for you!')
            
        # get best face
        options = tuple(faces)
        face    = self._face.replace(' ', '')
        
        if not face in options:
            for face in ('regular', 'book'):
                if face in options: 
                    self._face = face
                    break
            else: 
                face       = options[0]
                self._face = self._facetypes[0]
        
        # get and use path
        self._path  = faces.get(face, '')        
        self._font  = ImageFont.truetype(self._path, self._size, encoding=encoding)
        
        # inline
        return self
        
    # basic bbox
    def bbox(self, text:str) -> tuple:
        return self._font.getbbox(text)
    
    # smallest possible bbox
    def min_bbox(self, text:str) -> tuple:
        x, y, w, h = self._font.getbbox(text)
        return -x, -y, w-x, h-y
        
    # (right/bottom) margins mirror the (left/top) margins, respectively
    def max_bbox(self, text:str) -> tuple:
        x, y, w, h = self._font.getbbox(text)
        return 0, 0, w+x, h+y

