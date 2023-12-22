# SimPIL-Font
simplify loading remote fonts with PIL

## Basic Usage
```python3
from PIL import Image, ImageDraw
from simpilfont import SimPILFont

#you can use a list|tuple of font directories
sf = SimPILFont('C:/Windows/Fonts/')

#get ImageFont and dimensions of text
djvu_32   = sf("DejaVu Sans 32 bold").font  #DejaVu Sans 32 bold
_,_,w1,h1 = sf.max_bbox("Hello World")

#get ImageFont and dimensions of text
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

A font request has the signature `"family size face"` ex: `"Verdana 16 bold italic"`. A full font request will include all of these parts. Let's look at what can happen when you don't consider this.

```python3
from simpilfont import SimPILFont

sf = SimPILFont('C:/Windows/Fonts/')

print(sf('DejaVu Sans 16 bold')) # 'DejaVu Sans 16 bold'
print(sf('Verdana 12'))          # 'Verdana 12 bold'
```
Believe it or not, this is a feature. Every request is explicit.

```python3
print(sf('DejaVu Sans 16 bold'))    # 'DejaVu Sans 16 bold'
print(sf('12'))                     # 'DejaVu Sans 12 bold'
print(sf('condensed bold oblique')) # 'DejaVu Sans 12 condensed bold oblique'
print(sf('Impact 18 regular'))      # 'Impact 18 regular'
```

#### Font Data

`.family`, `.face`, `.size`, `.path`, `.options`, `.encoding`, and `.font` all return exactly what you would expect them to. `encoding` and `font` are the only 2 that can be set.

```python3
from simpilfont import SimPILFont

sf = SimPILFont('C:/Windows/Fonts/')

HELVETICA_22 = 'Helvetica 22 regular'
IMPACT_18    = 'Impact 18 regular'
VERDANA_16BI = 'Verdana 16 bold italic'

helvetica_22 = sf(HELVETICA_22).font
impact_18    = sf(IMPACT_18).font
verdana_16bi = sf(VERDANA_16BI).font

print(sf) # Verdana 16 bold italic

x,y,w,h = sf(IMPACT_18).bbox('Hello World')

print(sf) # Impact 18 regular

options = sf(HELVETICA_22).options  # ('regular', 'bold', 'italic', etc...)
path    = sf.path                   # "path/to/regular/helvetica.ttf"
```

#### BBox Variations
```python3
from simpilfont import SimPILFont

sf  = SimPILFont('C:/Windows/Fonts/')
ttf = sf("Verdana 20 regular").font

text = "Hello World"

#proxy for ImageFont.truetype(...).getbbox(text)
x1, y1, w1, h1 = sf.bbox(text)

#the smallest possible bbox
x2, y2, w2, h2 = sf.min_bbox(text)

#(right/bottom) margins mirror (left/top) margins, respectively
x3, y3, w3, h3 = sf.max_bbox(text)
```

