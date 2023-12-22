# SimPIL-Font
simplify loading remote fonts with PIL

## Basic Usage
```python3
from PIL import Image, ImageDraw
import simpilfont as font

SYSFONTS = 'C:/Windows/Fonts/'
DEJAVU32 = "DejaVu Sans 32 bold oblique"
        
text     = "Hello World"

sf       = font.Font(DEJAVU32, fontdirs=SYSFONTS)
djvu_32  = sf.font
x,y,w,h  = sf.max_bbox(text)

img      = Image.new("RGB", (w, h), color="black")
dctx     = ImageDraw.Draw(img)

dctx.text((x, y), text, font=djvu_32, fill="white")

img.show()
del dctx
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

You can use partial font descriptions. You shouldn't view font requests as a fresh request. You should always view it as modifying what is already there. For instance, every `Font` instance starts as `Arial 12` - if you request `Helvetica`, you will have `Helvetica 12`. This is an important thing to remember. What if you requested `DejaVu Sans 22 condensed bold oblique`, and then made a new request for `Impact 18` ~ what you really have is `Impact 18 condensed bold oblique`. That isn't going to exist. My system would catch that error and end up defaulting to `Impact 18 regular`, but know that you would actually be making a bad request. Any part of a font can be changed with a partial description.

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

#right now the font is 'Verdana 16 bold italic', but I need the bbox for 'Impact 18 regular'

x,y,w,h = sf(IMPACT_18).bbox('Hello World')

```

See how that works? Your constants are the font reference so, there is no reason to make multiple `Font` instances.
