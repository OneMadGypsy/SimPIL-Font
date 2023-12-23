# SimPIL-Font

A simple `"Family size face"` request system for `PIL.ImageFont.truetype(...)` 

## Basic Usage
```python3
from PIL import Image, ImageDraw
from simpilfont import SimPILFont

# you can alternately use a list|tuple of font directories
sf = SimPILFont('C:/Windows/Fonts/')

# get ImageFont and dimensions of text
djvu_32   = sf("DejaVu Sans 32 bold").font  #DejaVu Sans 32 bold
_,_,w1,h1 = sf.max_bbox("Hello World")

# get ImageFont and dimensions of text
djvu_27   = sf('27 book').font              #DejaVu Sans 27 book
_,_,w2,h2 = sf.max_bbox("Goodbye World")

img  = Image.new("RGB", (max(w1, w2), h1+h2), color="black")
dctx = ImageDraw.Draw(img)

dctx.text((0, 0) , "Hello World"  , font=djvu_32, fill="white")
dctx.text((0, h1), "Goodbye World", font=djvu_27, fill="red")

img.show()
del dctx
```

#### Font Requests

A font request has the signature `"family size face"` ex: `"Verdana 16 bold italic"`. Requests are explicit so, any part of a font can be changed. To be clearer, any part that you do not explicitly change, will not change.

```python3
from simpilfont import SimPILFont

sf = SimPILFont('C:/Windows/Fonts/')

print(sf('Verdana 16 bold'))        # 'Verdana 16 bold'
print(sf('DejaVu Sans'))            # 'DejaVu Sans 16 bold'
print(sf('12'))                     # 'DejaVu Sans 12 bold'
print(sf('condensed bold oblique')) # 'DejaVu Sans 12 condensed bold oblique'
print(sf('Impact regular'))         # 'Impact 12 regular'
```

#### Font Data

`.family`, `.face`, `.size`, `.path`, `.faces`, and `.font`, are the only properties. None of these properties have a setter.

```python3
from simpilfont import SimPILFont

sf = SimPILFont('C:/Windows/Fonts/')

# font request constants
IMPACT_18    = 'Impact 18 regular'
SYMBOL_16    = 'Symbol 16 regular'
VERDANA_16BI = 'Verdana 16 bold italic'
HELVETICA_22 = 'Helvetica 22 regular'

# ImageFont.FreeTypeFont instances
impact_18    = sf(IMPACT_18).font
symbol_16    = sf(SYMBOL, encoding="symb").font  # encoding is always "unic" unless otherwise specified
verdana_16bi = sf(VERDANA_16BI).font

# the currently loaded font is...
print(sf) # Verdana 16 bold italic

# load a different font and get some data
x,y,w,h = sf(IMPACT_18).bbox('Hello World')

# the currently loaded font is now...
print(sf) # Impact 18 regular

# once you make a font request, the SimPILFont instance retains all of the metadata until you make a new font request
helvetica_22 = sf(HELVETICA_22).font     # ImageFont.FreeTypeFont instance
faces        = sf.facetypes              # ('regular', 'bold', 'italic', etc...)
path         = sf.path                   # "path/to/regular/helvetica.ttf"
family       = sf.family                 # "Helvetica"
face         = sf.face                   # "regular"
size         = sf.size                   # 22
```

#### BBox Variations
```python3
from simpilfont import SimPILFont

sf  = SimPILFont('C:/Windows/Fonts/')
ttf = sf("Verdana 20 regular").font

text = "Hello World"

# proxy for ImageFont.truetype(...).getbbox(text)
x1, y1, w1, h1 = sf.bbox(text)

# the smallest possible bbox
x2, y2, w2, h2 = sf.min_bbox(text)

# (right/bottom) margins mirror (left/top) margins, respectively
x3, y3, w3, h3 = sf.max_bbox(text)
```

