# SimPIL-Font
simplify loading remote fonts with PIL

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


