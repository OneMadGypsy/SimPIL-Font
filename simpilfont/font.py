from __future__ import annotations
from glob       import iglob
from PIL        import ImageFont

import os, sys, json, functools

__all__ = ('Font',)

# common font directories for major systems
SYSTEMDIRS = dict(
    win32  = ('C:/Windows/Fonts', ),
    linux  = ('/usr/share/fonts', '/usr/local/share/fonts', '~/.local/share/fonts'),
    linux2 = ('/usr/share/fonts', '/usr/local/share/fonts', '~/.local/share/fonts'),
    darwin = ('/Library/Fonts'  , "/System/Library/Fonts" , os.path.expanduser("~/Library/Fonts")),
).get(sys.platform, tuple())


class Font:
    # https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
    ENCODINGS  = "unic", "symb", "lat1", "DOB", "ADBE", "ADBC", "armn", "sjis", "gb", "big5", "ans", "joha"
    ENC_EXCEPT = "Unable to encode font:\n\t({})"
    DNE_EXCEPT = ("Requested font family does not exist.\n"
                  "Call sf.export(), and check the resulting './fonts.json' file for your font request.")
        
    @property
    def family(self) -> str: 
        return getattr(self, '_family', 'Arial') or 'Arial'
        
    @property
    def style(self) -> str: 
        return getattr(self, '_style', 'regular') or 'regular'
        
    @property
    def size(self) -> int: 
        return getattr(self, '_size', 12) or 12
        
    @property
    def path(self) -> str: 
        return getattr(self, '_path', None)
        
    @property # supported styles for the current font 
    def styles(self) -> tuple: 
        return tuple(getattr(self, '_styles', None))
           
    @property
    def font(self) -> ImageFont.FreeTypeFont: 
        return getattr(self, '_font', None)
        
    def __init__(self, *args) -> None:
        self._fontdirs = tuple(set(map(os.path.abspath, args + SYSTEMDIRS)))
        
    def __str__(self) -> str:
        return ' '.join((self.family, f'{self.size}', self.style))
        
    def __call__(self, *request) -> Font:
        family, style, size = [], [], 0
        
        #parse font request
        for part in ' '.join(map(str, request)).split(' '):
            if part.isdigit(): size = int(part)
            else             : (style, family)[part != part.lower()].append(part)
                
        _family = (' '.join(family) or self.family).lower().replace(' ', '')
        _style  = (' '.join(style)  or self.style ).replace(' ', '')
        _faces  = (font := self.__get(_family)).get('faces', {})
            
        self._family = font['family']
        self._styles = font['styles']
        self._size   = size or self.size
        
        # set style - first to exist from this order: requested, regular, book, first style
        for _ in self._styles:
            if _style == _.replace(' ', ''):
                self._style = _
                break
        else:
            options = tuple(_faces)
            
            for _ in ('regular', 'book'):
                if _ in options: 
                    self._style = _
                    break
            else: 
                self._style = self._styles[0]
            
        # get and use path 
        _style     = self._style.replace(' ', '')
        self._path = _faces.get(_style, '')
        self._font = ImageFont.truetype(self._path, self._size, encoding=font['encoding'])
        
        # inline
        return self
    
    def __enc(self, fn:string) -> tuple:
        #whack-a-mole
        for encoding in Font.ENCODINGS:
            try   : ttf = ImageFont.truetype(font=fn, encoding=encoding)
            except: continue
            else  :
                family, style = ttf.getname() 
                return encoding, family, style
                
        raise Exception(Font.ENC_EXCEPT.format(fn))
    
    @functools.cache
    def __get(self, fam:str) -> dict:
        found = False
        
        t_family, t_styles, t_faces  = fam, list(), dict()
        
        # find all styles of a family
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/{fam[0:2]}*.ttf', recursive=True):
                fn = os.path.abspath(fn)
                
                encoding, family, style = self.__enc(fn)
                    
                if fam == family.lower().replace(' ', ''):
                    style, found = style.lower(), True
                    
                    t_family = family  
                    t_faces[style.replace(' ', '')] = fn
                    t_styles.append(style)
                            
                elif found: break
                    
            if found: break
            
        else: raise Exception(Font.DNE_EXCEPT)
        
        return dict(family=t_family, styles=t_styles, faces=t_faces, encoding=encoding)
        
    def export(self) -> None:
        out = {k:[] for k in Font.ENCODINGS}
        
        for directory in self._fontdirs:
            for fn in iglob(fr'{directory}**/*.ttf', recursive=True):
                encoding, family, style = self.__enc(os.path.abspath(fn))
                out[encoding].append(f'{family} {style.lower()}')
                    
        with open('fonts.json', 'w') as f:
            f.write(json.dumps(out, indent=4))
            
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