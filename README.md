# SimPILFont

A `"family size style"` request system for `PIL.ImageFont.truetype(...)`. 

## Basic Usage
```python3
from PIL import Image, ImageDraw
from simpilfont import SimPILFont

# instance with zero or more paths to *non-obvious font directories
#  *platform-specific font directories are already known
sf = SimPILFont('./fonts', './some_other/fonts')

# get ImageFont and dimensions of text
text_32   = "Hello World"
djvu_32   = sf("DejaVu Sans 32 bold").font  # 'DejaVu Sans 32 bold'
_,_,w1,h1 = sf.max_bbox(text_32)

# get ImageFont and dimensions of text
text_27   = "Goodbye World"
djvu_27   = sf("27 book").font  # 'DejaVu Sans 27 book'
_,_,w2,h2 = sf.max_bbox(text_27)

img  = Image.new("RGB", (max(w1, w2), h1+h2), color="black")
dctx = ImageDraw.Draw(img)

dctx.text((0, 0) , text_32, font=djvu_32, fill="white")
dctx.text((0, h1), text_27, font=djvu_27, fill="red")

img.show()
del dctx
```

## Font Requests

A font request has the signature `"family size style"` ex: `"Verdana 16 bold italic"`. Requests are explicit. Any part that you do not explicitly change, will not change. Subsequent requests for a family will receive cached data that was memoized when the family was first requested. Font encoding is determined internally. You never need to consider it.

```python3
from simpilfont import SimPILFont

sf = SimPILFont()

print(sf('Verdana 16 bold'))        # 'Verdana 16 bold'
print(sf('DejaVu Sans'))            # 'DejaVu Sans 16 bold'
print(sf('12'))                     # 'DejaVu Sans 12 bold'
print(sf('condensed bold oblique')) # 'DejaVu Sans 12 condensed bold oblique'
print(sf('Impact regular'))         # 'Impact 12 regular'
```

Font requests can also be formatted as `args`, and the order of your arguments, in either style font request, don't actually matter.

```python3
from simpilfont import SimPILFont

sf = SimPILFont()

print(sf('Verdana', 'bold', 16))  # 'Verdana 16 bold'
print(sf('bold DejaVu Sans 22'))  # 'DejaVu Sans 22 bold'

# technically, even this would work. it's an unintended byproduct of my parse method and is not a recommended format 
print(sf('condensed DejaVu bold 22 oblique Sans'))  # 'DejaVu Sans 22 condensed bold oblique'
```

Every part of `family.split(' ')` must include one or more capital letters. Every part of `style.split(' ')` must be entirely lowercase. As long as you mind the rules you can make some mistakes.

```python3
from simpilfont import SimPILFont

sf = SimPILFont()

#printing always returns the font request as the "perfect" request 
print(sf('De Javu Sans 16 extra light')) # 'DejaVu Sans 16 extralight'
print(sf.styles)                         # ('bold', 'bold oblique', 'extralight', 'oblique', 'book', 'condensed bold', 'condensed bold oblique', 'condensed oblique', 'condensed')
```

## Font Data

| property| description                    | default    |
|---------|--------------------------------|------------|
|`.family`| family name                    | "Arial"    |
|`.style` | style name                     | "regular"  |
|`.size`  | font size                      | 12         |
|`.path`  | path to font file              | None       |
|`.font`  | ImageFont.FreeTypeFont instance| None       |
|`.styles`| tuple of supported styles      | None       |

```python3
from simpilfont import SimPILFont

sf = SimPILFont()

# font request constants
HELVETICA_22 = 'Helvetica 22 regular'

# once you make a font request, the SimPILFont instance retains all of the metadata until you make a new font request
# a font request is the only way to affect these properties
helvetica_22 = sf(HELVETICA_22).font  # ImageFont.FreeTypeFont instance
styles       = sf.styles              # ('regular', 'bold', 'italic', etc...)
path         = sf.path                # "path/to/regular/helvetica.ttf"
family       = sf.family              # "Helvetica"
style        = sf.style               # "regular"
size         = sf.size                # 22
```

You can call the inline `.export()` method to save a json file, containing all compatible fonts, categorized by their encoding.

```python3
from simpilfont import SimPILFont

#export returns the SimPILFont instance
sf = SimPILFont().export()    # saved to app_directory/fonts.json
```

## BBox Variations
```python3
from simpilfont import SimPILFont

# you can use this shortcut if you want to instance SimPILFont and request a "start-up" font
# this makes more sense if you only intend to use one font - like this example
sf  = SimPILFont()("Verdana 20 regular")

text = "Hello World"

# proxy for ttf.getbbox(text)
x1, y1, w1, h1 = sf.bbox(text)

# the smallest possible bbox
x2, y2, w2, h2 = sf.min_bbox(text)

# (right/bottom) margins mirror (left/top) margins, respectively
x3, y3, w3, h3 = sf.max_bbox(text)
```

