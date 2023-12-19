# SimPIL-Font
simplify loading remote fonts with PIL

## Basic Usage
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

text    = "Hello World"

sf      = SimPILFont('ABeeZee 32 regular')
x,y,w,h = sf.bbox(text)

img  = Image.new("RGB", (w-x, h-y), color="black")
dctx = ImageDraw.Draw(img)

dctx.text((-x, -y), text, font=sf.font, fill="white")

img.show()
del dctx
```

## Extra
Dump fontmap to `./fonts.json`. 
> The below example is also setting `fontdir`, but that isn't required if fonts are already loaded.
> The dump will be the entire dict, including the new font data from `fontdir` (if used).
> The resulting `fonts.json` is never used with any part of the font system. It's only purpose is to be a convenience if you needed a hard-copy.

```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts', dumpmap=True)
```

Partial font changes
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

sf      = SimPILFont('Consolas 32')
sf.font = 'bold'        # Consolas 32 bold
sf.font = 'Verdana'     # Verdana 32 bold
sf.font = '18 italic'   # Verdana 18 italic
sf.font = 'bold italic' # Verdana 18 bold italic
sf.font = '12'          # Verdana 12 bold italic
```

ImageFont instance without SimPILFont instance
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

ttf = SimPILFont.instance('Verdana 32 bold')
```

## Facts
* You can call `FONTMAP` with a new `fontdir` as many times as you like. All the new font metadata will be pooled with the existing font data.
  
  ```python3
  FONTMAP(fontdir="these/fonts/")
  FONTMAP(fontdir="those/fonts/")
  FONTMAP(fontdir="other/fonts/")
  ```
* The underlying `FONTMAP` dict singleton is formatted like the object below:
  
  ```json
  {
      "Family Name": {
          "face": "path/to/this_face.ttf",
      },
      "DejaVu Sans": {
        "bold": "c:/Windows/Fonts\\DejaVuSans-Bold.ttf",
        "bold oblique": "c:/Windows/Fonts\\DejaVuSans-BoldOblique.ttf",
        "extralight": "c:/Windows/Fonts\\DejaVuSans-ExtraLight.ttf",
        "oblique": "c:/Windows/Fonts\\DejaVuSans-Oblique.ttf",
        "book": "c:/Windows/Fonts\\DejaVuSans.ttf",
        "condensed bold": "c:/Windows/Fonts\\DejaVuSansCondensed-Bold.ttf",
        "condensed bold oblique": "c:/Windows/Fonts\\DejaVuSansCondensed-BoldOblique.ttf",
        "condensed oblique": "c:/Windows/Fonts\\DejaVuSansCondensed-Oblique.ttf",
        "condensed": "c:/Windows/Fonts\\DejaVuSansCondensed.ttf"
      }
  }
  ```
  This is a generalization of what the backend does when you request a font
  
  ```python3
  family = 'DejaVu Sans'
  face   = 'condensed bold oblique'
  path   = FONTMAP(family)[face]
  ttf    = ImageFont.truetype(path, ...)
  ```
* If you request a face that does not exist, `"regular"` will be attempted else `"book"` will be attempted else the first face in the family. You can check the faces available for a font with the `.faces` property.
  
  ```python3
  sf = SimPILFont('DejaVu Sans 32 extra light') #should be extralight
  print(sf.faces) # ('bold', 'bold oblique', 'extralight', 'oblique', 'book', 'condensed bold', 'condensed bold oblique', 'condensed oblique', 'condensed')
  print(sf)       # DejaVu Sans 32 book
  ```
* `encoding` can be set in the constructor or `.instance` method. The default is `"unic"`. The encoding must be valid or it will default to `"unic"`. For information on valid encodings see: https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
  
  ```python3
  sf  = SimPILFont('Symbol 16', encoding='symb')
  ttf = SimPILFont.instance('Symbol 16', encoding='symb')
  ```
* tkinter font format is barely supported - fails if `overstrike` or `underline` are included
  
  ```python3
  sf  = SimPILFont('{Times New Roman} 32 bold')
  ttf = SimPILFont.instance('{Times New Roman} 32 bold')
  ```
* If you are on windows, `C:/Windows/Fonts` directory is automatically loaded. If that's all you need, it is unnecessary to call `FONTMAP`. There is a spot reserved for "Linux" and "Darwin" to do the same thing, but I didn't know the directories to use, and have no way to test them. If you are on one of those systems, adjust [`FONTDIR`](https://github.com/OneMadGypsy/SimPIL-Font/blob/main/simpilfont.py#L27) accordingly.
  ```python3
  #line 27 of simpilfont.py
  FONTDIR = {
    "Windows": "c:/Windows/Fonts/",
    #"Darwin" : "",
    #"Linux"  : ""
  }.get(platform.system(), '')
  ```
* There are some properties and staticmethods that weren't covered in this README. The code is not even 200 lines. You can browse it and easily figure out the stuff that was skipped. It's mostly stuff like `.family`, `.size`, `.face`, etc.. Printing a `SimPILFont` instance can tell you all of that in one shot. `.font` and `encoding` are the only properties with a setter. Setting `.encoding` will not update `.font`. 
  
  ```python3
  #to string
  print(sf) # Times New Roman 32 bold

  #encoding after font has already been made
  sf.encoding = "symb"
  sf.font     = str(sf)
  ```


