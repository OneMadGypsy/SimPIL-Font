from __future__ import annotations
from glob       import iglob
from typing     import Iterable
from functools  import cache
from PIL        import ImageFont
import os


class SimPILFont:
    # https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
    ENCODINGS = "unic", "symb", "DOB", "ADBE", "ADBC", "armn", "sjis", "gb", "big5", "ans", "joha", "lat1"
    EXCEPTION = 'No font. You may be using the wrong encoding for this font. The default is "unic".'
        
    @property
    def family(self) -> str: 
        return getattr(self, '_family', 'Arial') or 'Arial'
        
    @property
    def face(self) -> str: 
        return getattr(self, '_face', 'regular') or 'regular'
        
    @property
    def size(self) -> int: 
        return getattr(self, '_size', 12) or 12
        
    @property
    def path(self) -> str: 
        return getattr(self, '_path', None)
        
    @property # supported faces for the current font 
    def facetypes(self) -> tuple: 
        return tuple(getattr(self, '_facetypes', None))
           
    @property
    def font(self) -> ImageFont.FreeTypeFont: 
        return getattr(self, '_font', None)
        
    def __init__(self, fontdirs:Iterable) -> None:
        self._fontdirs = fontdirs if isinstance(fontdirs, list|tuple) else (fontdirs, )
        
    def __str__(self) -> str:
        return ' '.join((self.family, f'{self.size}', self.face))
        
    def __call__(self, font:str, encoding:str='unic') -> SimPILFont:
        encoding = encoding if encoding in SimPILFont.ENCODINGS else 'unic'
        
        # get details
        family, face, size = [], [], 0
        
        for part in font.split(' '):
            if part.isdigit(): size = int(part)
            else             : (face, family)[part != part.lower()].append(part)
                
        _family = (' '.join(family) or self.family).lower().replace(' ', '')
        _face   = (' '.join(face)   or self.face  ).replace(' ', '')
        item    = self.__(_family, encoding)
            
        faces           = item['faces']
        self._family    = item['family']
        self._facetypes = item['facetypes']
        self._size      = size or self.size
        
        for ft in self._facetypes:
            if _face == (face := ft.replace(' ', '')):
                self._face = ft
                break
        else:
            options = tuple(faces)
            
            for face in ('regular', 'book'):
                if face in options: 
                    self._face = face
                    break
            else: 
                face       = options[0]
                self._face = self._facetypes[0]
            
        # get and use path
        self._path = faces.get(face, '') 
        self._font = ImageFont.truetype(self._path, self._size, encoding=encoding)
        
        # inline
        return self
    
    @cache
    def __(self, fam:str, encoding:str="unic") -> dict:
        found = False
        
        t_family, t_facetypes, t_faces  = fam, list(), dict()
        
        # find font via family and face
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/{fam[0:2]}*.ttf', recursive=True):
                fn = os.path.abspath(fn)
                
                try   : ttf = ImageFont.truetype(font=fn, encoding=encoding)
                except: ...
                else  :
                    family, face = ttf.getname() 
                    
                    if fam == family.lower().replace(' ', ''):
                        face, found = face.lower(), True
                        
                        t_family = family  
                        t_faces[face.replace(' ', '')] = fn
                        t_facetypes.append(face)
                            
                    elif found: break
                    
            if found: break
            
        else: raise Exception(SimPILFont.EXCEPTION)
        
        return dict(family=t_family, facetypes=t_facetypes, faces=t_faces)
        
    def export(self) -> None:
        out = {k:[] for k in SimPILFont.ENCODINGS}
        
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/*.ttf', recursive=True):
                fn = os.path.abspath(fn)
                
                for enc in SimPILFont.ENCODINGS:
                    try   : ttf = ImageFont.truetype(font=fn, encoding=enc)
                    except: ...
                    else  :
                        family, face = ttf.getname() 
                        out[enc].append(f'{family} {face.lower()}')
                        break
                    
        with open('fonts.json', 'w') as f:
            f.write(json.dumps(out, indent=4))
                    
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
