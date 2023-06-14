from subprocess import Popen, PIPE
from os import remove
from PIL import Image
import os

#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [135, 206, 235] #[255, 255, 255]

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        #print([DEFAULT_COLOR[i] * y / 500 for i in range(3)])
        for x in range( width ):
            #screen[y].append( [DEFAULT_COLOR[i] * y / 500 for i in range(3)] )
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

def new_zbuffer( width = XRES, height = YRES ):
    zb = []
    for y in range( height ):
        row = [ float('-inf') for x in range(width) ]
        zb.append( row )
    return zb

def plot( screen, zbuffer, color, x, y, z, supersample = 1 ):
    width = XRES * supersample
    height = YRES * supersample
    newy = height - 1 - y
    z = int((z * 1000)) / 1000.0
    if ( x >= 0 and x < width and newy >= 0 and newy < height and z - zbuffer[newy][x] >= -1):
        screen[newy][x] = color[:]
        zbuffer[newy][x] = z

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]

def clear_zbuffer( zb ):
    for y in range( len(zb) ):
        for x in range( len(zb[y]) ):
            zb[y][x] = float('-inf')

def save_ppm( screen, fname ):
    f = open( fname, 'wb' )
    ppm = 'P6\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    f.write(ppm.encode())
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            f.write( bytes(pixel) )
    f.close()

def save_ppm_ascii( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()

def save_extension( screen, fname ):
    img = Image.new('RGB', (len(screen[0]), len(screen)))

    pixels = []
    for row in screen:
        for pixel in row:
            pixels.append( tuple(pixel) )

    img.putdata(pixels)
    img.save(fname, 'PNG')

def display( screen ):
    img = Image.new('RGB', (len(screen[0]), len(screen)))

    pixels = []
    for row in screen:
        for pixel in row:
            pixels.append( tuple(pixel) )

    img.putdata(pixels)
    img.show()

def convert_to_gif( basename, gif ):
    os.system("magick -delay 20 %s* %s" % (basename, gif))

def show_gif( gif ):
    os.system("open %s" % gif)
