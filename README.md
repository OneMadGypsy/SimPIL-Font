# SimPIL-Font
simplify loading remote fonts with PIL

## Basic Usage
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

text    = "Hello World"

ttf     = SimPILFont('ABeeZee 32 regular')
x,y,w,h = ttf.bbox(text)

img  = Image.new("RGB", (w-x, h-y), color="black")
dctx = ImageDraw.Draw(img)

dctx.text((-x, -y), text, font=ttf.font, fill="white")

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

ttf      = SimPILFont('Consolas 32')
ttf.font = 'bold'        # Consolas 32 bold
ttf.font = 'Verdana'     # Verdana 32 bold
ttf.font = '18 italic'   # Verdana 18 italic
ttf.font = 'bold italic' # Verdana 18 bold italic
ttf.font = '12'          # Verdana 12 bold italic
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

ttf = SimPILFont('Consolas 32 bold')
print(ttf) # Consolas 32 bold
```

## Facts

* Every time you call `FONTMAP` with the `fontdir` argument, the directory and all of it's subdirectories are scraped for `.ttf` files. The metadata for those files is added to the underlying `FONTMAP` dict.
* `encoding` can be set in the constructor or `.instance` method. The default is `"unic"`. The encoding must be valid or it will default to `"unic"`. For information on valid encodings see: https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
* If you are on windows `C:/Windows/Fonts` directory is automatically loaded, and if that's all you need, there is no need to call `FONTMAP`. There is a spot reserved for "Linux" and "Darwin" to do the same thing, but I didn't know the directories to use, and have no way to test them. If you are on one of those systems, uncomment your system in the [`FONTDIR`](https://github.com/OneMadGypsy/SimPIL-Font/blob/main/simpilfont.py#L27) constant and set the appropriate path as the value. 

