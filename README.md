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
Dump fontmap to fonts.json
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

Accepts tkinter font format - but will fail if `overstrike` or `underline` are included
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

ttf = SimPILFont.instance('{Times New Roman} 32 bold')
```

To string
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

sf = SimPILFont('Consolas 32 bold')
print(sf) # Consolas 32 bold
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
        "extralight": "c:/Windows/Fonts\\DejaVuSans-ExtraLight.ttf", //you may expect a space in the key that isn't actually there
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
  sf  = SimPILFont('Symbol', encoding='symb')
  ttf = SimPILFont.instance('Symbol', encoding='symb')
  ```
* If you are on windows, `C:/Windows/Fonts` directory is automatically loaded. If that's all you need it is unnecessary to call `FONTMAP`. There is a spot reserved for "Linux" and "Darwin" to do the same thing, but I didn't know the directories to use, and have no way to test them. If you are on one of those systems, adjust [`FONTDIR`](https://github.com/OneMadGypsy/SimPIL-Font/blob/main/simpilfont.py#L27) accordingly.


