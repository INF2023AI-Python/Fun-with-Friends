
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
matrix = RGBMatrix(options = options)
offset_canvas = matrix.CreateFrameCanvas()

a = 6
while a < 28:
    b = 8
    while b < 26: 
        offset_canvas.SetPixel(a, b, 255, 255, 255)  
        offset_canvas = matrix.CreateFrameCanvas()
        b += 3
    
    a += 1
c = 6
while c < 28:
    offset_canvas.SetPixel(25, c, 255, 255, 255)
    offset_canvas = matrix.CreateFrameCanvas()
    c += 1

