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
dump fontmap to "fonts.json"
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts', dumpmap=True)
```

partial font changes
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

ImageFont without SimPILFont instance
```python3
from simpilfont import SimPILFont, FONTMAP

FONTMAP(fontdir='path/to/fonts')

ttf = SimPILFont.instance('Verdana 32 bold')
```


