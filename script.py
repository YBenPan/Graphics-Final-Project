import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    # view = [0,
    #         0,
    #         1]
    # ambient = [50,
    #            50,
    #            50]
    # light = [[0.5,
    #           0.75,
    #           1],
    #          [255,
    #           255,
    #           255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    # Unpack lights from symbol table and normalize location vectors
    lights = [ [v[1]['location'], v[1]['color']] for v in symbols.values() if v[0] == 'light']
    if not lights: 
        lights.append([[0.5, 0.75, 1], [255, 255, 255]])
    for light in lights: 
        normalize(light[LOCATION])
    # print(lights)

    # Set ambient light
    ambient = symbols['ambient'][1:] if 'ambient' in symbols else [50, 50, 50]

    # Set camera
    view = symbols['camera'][1]['aim'] if 'camera' in symbols and 'aim' in symbols['camera'][1] else [0, 0, 1]
    
    print("All symbols:")
    print(symbols)
    input()

    for command in commands:
        print(command)
        c = command['op']
        args = command['args']

        if c == 'box':
            if command['constants']:
                reflect = command['constants']
            add_box(tmp,
                    args[0], args[1], args[2],
                    args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect)
            tmp = []
            reflect = '.white'
        elif c == 'sphere':
            if command['constants']:
                reflect = command['constants']
            add_sphere(tmp,
                       args[0], args[1], args[2], args[3], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect)
            tmp = []
            reflect = '.white'
        elif c == 'torus':
            if command['constants']:
                reflect = command['constants']
            add_torus(tmp,
                      args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect)
            tmp = []
            reflect = '.white'
        elif c == 'line':
            add_edge(tmp,
                     args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult( stack[-1], tmp )
            draw_lines(tmp, screen, zbuffer, color)
            tmp = []
        elif c == 'mesh':
            # input()
            filename = f"{command['args'][0]}.obj"
            vertexList = []
            faceList = []
            with open(filename) as file:
                for line in file:
                    line = line.rstrip()
                    if line[:2] == 'v ':
                        vertexList.append([float(coord) for coord in line[2:].split()])
                    elif line[:2] == 'f ':
                        faceList.append([int(vertex) - 1 for vertex in line[2:].split()])
            add_mesh(tmp, vertexList, faceList)
            matrix_mult( stack[-1], tmp )
            draw_polygons(tmp, screen, zbuffer, view, ambient, lights, symbols, reflect)
            tmp = []
            # input()

        elif c == 'move':
            tmp = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'scale':
            tmp = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], tmp)
            stack[-1] = [x[:] for x in tmp]
            tmp = []
        elif c == 'rotate':
            theta = args[1] * (math.pi/180)
            if args[0] == 'x':
                tmp = make_rotX(theta)
            elif args[0] == 'y':
                tmp = make_rotY(theta)
            else:
                tmp = make_rotZ(theta)
            matrix_mult( stack[-1], tmp )
            stack[-1] = [ x[:] for x in tmp]
            tmp = []
        elif c == 'push':
            stack.append([x[:] for x in stack[-1]] )
        elif c == 'pop':
            stack.pop()
        elif c == 'display':
            display(screen)
        elif c == 'save':
            save_extension(screen, args[0])