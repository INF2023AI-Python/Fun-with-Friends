
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

a = 6
while a < 28:
    b = 8
    while b < 26: 
        offset_canvas.SetPixel(a, b, 255, 255, 255)  
        offset_canvas = matrix.CreateFrameCanvas(offset_canvas)
        b += 3
    
    a += 1
c = 6
while c < 28:
    offset_canvas.SetPixel(25, c, 255, 255, 255)
    offset_canvas = matrix.CreateFrameCanvas(offset_canvas)
    c += 1

