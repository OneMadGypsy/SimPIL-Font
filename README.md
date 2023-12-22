# SimPIL-Font
simplify loading remote fonts with PIL

## Basic Usage
```python3
from PIL import Image, ImageDraw
import simpilfont as font

SYSFONTS = 'C:/Windows/Fonts/'
DEJAVU32 = "DejaVu Sans 32 bold"
        
"""
The database will only be updated if:
  * the `fontdirs` path(s) has never been scraped
  * the `fontdirs` path(s) has a newer modification date than it's database entry 
"""
sf = font.Font(fontdirs=SYSFONTS)

#get ImageFont
djvu_32     = sf(DEJAVU32).font          #DejaVu Sans 32 bold
x1,y1,w1,h1 = sf.max_bbox("Hello World")

djvu_27     = sf('27 book').font         #DejaVu Sans 27 book
x2,y2,w2,h2 = sf.max_bbox("Goodbye World")

img  = Image.new("RGB", (max(w1, w2), h1+h2+y1+y2), color="black")
dctx = ImageDraw.Draw(img)

dctx.text((x1, y1)   , "Hello World"  , font=djvu_32, fill="white")
dctx.text((x1, h1+y2), "Goodbye World", font=djvu_27, fill="red")

img.show()
```

#### Font Retrieval
```python3
import simpilfont as font

sf = font.Font()

#inline
helvetica_22  = sf('Helvetica 22').font # Helvetica
helvetica_22b = sf('bold').font         # Helvetica bold

#alternative
sf.font       = 'Helvetica 22'
helvetica_22  = sf.font  # Helvetica

sf.font       = 'bold'   # inherits what it doesn't change ~ same for the inline method
helvetica_22b = sf.font  # Helvetica bold
```

#### BBox Variations
```python3
import simpilfont as font

sf = font.Font('Verdana 18')

text = "Hello World"

#proxy for ImageFont.truetype(...).getbbox(text)
x1, y1, w1, h1 = sf.bbox(text)

#the smallest possible bbox
x2, y2, w2, h2 = sf.min_bbox(text)

#(right/bottom) margins mirror (left/top) margins, respectively
x3, y3, w3, h3 = sf.max_bbox(text)
```


----------------

## Details

When you call `Font` with a `fontdirs` argument, this system checks the database for the directory. If it exists, modification dates are compared. If the database has an old modification date for this directory or the directory has never been scraped, the directory and all subdirectories are scraped for '.ttf' fonts. This means you only need to supply `fontdirs` values, once ... ever. 

The absolute very first time you ever import `simpilfont`, it will create a `./dat/` directory and put a database in it. It also creates a `./dat/fonts/` directory. Copy fonts to `./dat/fonts/`, and on the next run of `Font()`, they will be found and registered in the database. If you intend to go this route, you never have to use the `fontdirs` argument.

font requests have the signature `"family size face"` ex: `"Verdana 16 bold italic"`. A full font request will include all of these parts, including `"regular"` when you do not want a modified face. Let's look at what can happen when you don't consider this.

```python3
import simpilfont as font

sf = font.Font()

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

You can create multiple `Font` instances, but there is no good reason to. The `Font` class is the front-end to your database. It's dressed up real pretty like it's trying to be a font instance, but It's really EVERY font instance. Using the inline request method you can return anything you need to know about a font, including the font, and even the bbox methods for that font. 

```python3
import simpilfont as font

HELVETICA_22 = 'Helvetica 22 regular'
IMPACT_18    = 'Impact 18 regular'
VERDANA_16BI = 'Verdana 16 bold italic'

sf = font.Font()

helvetica_22 = sf(HELVETICA_22).font
impact_18    = sf(IMPACT_18).font
verdana_16bi = sf(VERDANA_16BI).font

print(sf) # Verdana 16 bold italic - but I need the bbox for IMPACT_18

x,y,w,h = sf(IMPACT_18).bbox('Hello World')

print(sf) # Impact 18 regular - but I need the options for HELVETICA_22

options = sf(HELVETICA_22).options  # (regular, bold, italic, etc...)

```

You get the point. Your constants are the font reference so, there is no reason to make multiple `Font` instances.
