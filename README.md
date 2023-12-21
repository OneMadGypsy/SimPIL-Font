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

#### Inline Font Retrieval
```python3
import simpilfont as font

sf = font.Font()

helvetica_22  = sf('Helvetica 22').font # Helvetica
helvetics_22b = sf('bold').font         # Helvetica bold
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

The absolute very first time you ever use `Font()`, it will create a `./dat/` directory and put a `shelve` database in it. It also creates a `./dat/fonts/` directory. Copy fonts to `./dat/fonts/`, and on the next run of `Font()`, they will be found and registered in the database. If you intend to go this route, you never have to use the `fontdirs` argument.



