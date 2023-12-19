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

ttf      = SimPILFont('Verdana 32')
ttf.font = 'bold'     # Verdana 32 bold
ttf.font = 'Consolas' # Consolas 32 bold
ttf.font = '18'       # Consolas 18 bold
```


