from __future__ import annotations
from glob       import iglob
from typing     import Iterable, Iterator
from functools  import cache
from PIL        import ImageFont
import os, json


class SimPILFont:
    # https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
    ENCODINGS = "unic", "symb", "lat1", "DOB", "ADBE", "ADBC", "armn", "sjis", "gb", "big5", "ans", "joha"
    EXCEPTION = 'No font. You may be using the wrong encoding for this font. The default encoding is "unic".'
        
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
        
    def __init__(self, *args) -> None:
        self._fontdirs = args
        
    def __str__(self) -> str:
        return ' '.join((self.family, f'{self.size}', self.face))
        
    def __call__(self, *request) -> SimPILFont:
        family, face, size = [], [], 0
        
        #parse font request
        for part in ' '.join(request).split(' '):
            if part.isdigit(): size = int(part)
            else             : (face, family)[part != part.lower()].append(part)
                
        _family = (' '.join(family) or self.family).lower().replace(' ', '')
        _face   = (' '.join(face)   or self.face  ).replace(' ', '')
        
        item = self.__(_family)
            
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
        self._font = ImageFont.truetype(self._path, self._size, encoding=item['encoding'])
        
        # inline
        return self
    
    def __enc(self, fn:string) -> tuple:
        for encoding in SimPILFont.ENCODINGS:
            try   : ttf = ImageFont.truetype(font=fn, encoding=encoding)
            except: continue
            else  :
                family, face = ttf.getname() 
                return encoding, family, face
    
    @cache
    def __(self, fam:str) -> dict:
        found = False
        
        t_family, t_facetypes, t_faces  = fam, list(), dict()
        
        # find all faces of a family
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/{fam[0:2]}*.ttf', recursive=True):
                fn = os.path.abspath(fn)
                
                encoding, family, face = self.__enc(fn)
                    
                if fam == family.lower().replace(' ', ''):
                    face, found = face.lower(), True
                    
                    t_family = family  
                    t_faces[face.replace(' ', '')] = fn
                    t_facetypes.append(face)
                            
                elif found: break
                    
            if found: break
            
        else: raise Exception(SimPILFont.EXCEPTION)
        
        return dict(family=t_family, facetypes=t_facetypes, faces=t_faces, encoding=encoding)
        
    def export(self) -> None:
        out = {k:[] for k in SimPILFont.ENCODINGS}
        
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/*.ttf', recursive=True):
                encoding, family, face = self.__enc(os.path.abspath(fn))
                out[encoding].append(f'{family} {face.lower()}')
                    
        with open('fonts.json', 'w') as f:
            f.write(json.dumps(out, indent=4))
            
        #inline method
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
