from   glob    import iglob
from   typing  import Iterable
from   PIL     import ImageFont
import os

class SimPILFont:
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
        
    @property #current family
    def family(self) -> str:
        return self._family
        
    @property #current face
    def face(self) -> str:
        return self._face
        
    @property #current size
    def size(self) -> int:
        return self._size
        
    @property #current path
    def path(self) -> str:
        return self._path
        
    @property #list of supported faces for the current font 
    def faces(self) -> tuple:
        return tuple(self._faces)
           
    @property #current ImageFont encoding
    def encoding(self) -> str:
        return self._encoding
        
    @property #current ImageFont instance
    def font(self) -> ImageFont.FreeTypeFont:
        return self._font
        
    ## DUNDER
        
    def __init__(self, fontdirs:Iterable, encoding:str="unic"):
        self._fontdirs = fontdirs if isinstance(fontdirs, list|tuple) else (fontdirs, )
        self._encoding = encoding if encoding in SimPILFont.ENCODINGS else 'unic'
        
    def __str__(self) -> str:
        return ' '.join((self._family, f'{self._size}', self._face))
        
    def __call__(self, font:str, encoding:str|None=None):
        enc            = encoding or self._encoding
        self._encoding = enc if enc in SimPILFont.ENCODINGS else 'unic'
        
        #get details
        family, face, size = SimPILFont.metadata(font)
        
        #use detail else nochange else default
        self._family  = family or getattr(self, '_family', 'Arial')
        self._size    = size   or getattr(self, '_size'  , 12)
        self._face    = face   or getattr(self, '_face'  , 'regular')
        
        faces       = dict()
        found       = False
        self._faces = []
        
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/*.ttf', recursive=True):
                fn = os.path.abspath(fn)
                try:
                    ttf = ImageFont.truetype(font=fn)
                except: ...
                else:
                    family, face = ttf.getname() 
                    
                    if (family != self._family) and found:
                        break
                    
                    if family == self._family:
                        found = True
                        face  = face.lower()
                        self._faces.append(face)
                        faces[face.replace(' ', '')] = fn
                    
            if found: 
                break
        else: 
            raise ValueError('No font for you!')
            
        #juggle face type
        face = SimPILFont.bestface(self._face, tuple(faces))
        
        for option in self._faces:
            if option.replace(' ', '') == face:
                self._face = option
                break
        
        self._path  = faces.get(face, '')        
        self._font  = ImageFont.truetype(self._path, self._size, encoding=self._encoding)
        
        return self
        
    ## PROXIES
       
    #basic bbox
    def bbox(self, text:str) -> tuple:
        return self._font.getbbox(text)
    
    #smallest possible bbox
    def min_bbox(self, text:str) -> tuple:
        x, y, w, h = self._font.getbbox(text)
        return -x, -y, w-x, h-y
        
    #(right/bottom) margins mirror the (left/top) margins, respectively
    def max_bbox(self, text:str) -> tuple:
        x, y, w, h = self._font.getbbox(text)
        return 0, 0, w+x, h+y
