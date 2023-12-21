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
sf = font.Font()

helvetica_22  = sf('Helvetica 22').font # Helvetica
helvetics_22b = sf('bold').font         # Helvetica bold
```

#### BBox Variations
```python3
sf = font.Font('Verdana 18')

text = "Hello World"

#proxy for ttf.getbbox(text)
x1, y1, w1, h1 = sf.bbox(text)

#the smallest possible bbox
x2, y2, w2, h2 = sf.min_bbox(text)

#(right/bottom) margins mirror (left/top) margins, respectively
x3, y3, w3, h3 = sf.max_bbox(text)
```



