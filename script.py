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

    # Check for animation keywords
    frames = False
    basename = False
    vary = False

    print("All symbols:")
    print(symbols)
    input()

    # Pass 0
    for command in commands:
        c = command['op']
        args = command['args']

        if c == 'vary':
            vary = True

        elif c == 'frames':
            frames = int(args[0])

        elif c == 'basename':
            basename = args[0]

    if vary and not frames:
        print("MDL Compiler Error")
        return

    if frames and not basename:
        print("Warning: Animation basename not entered.")
        basename = 'basename'

    # Pass 1

    if frames:
        knoblist = [{} for i in range(frames)]
    else:
        frames = 1

    for command in commands:
        c = command['op']
        args = command['args']

        if c == 'vary':
            knob = command['knob']
            start_frame = int(args[0])
            end_frame = int(args[1])
            start_value = args[2]
            end_value = args[3]
            value_delta = (end_value-start_value)/(end_frame-start_frame-1)

            knoblist[start_frame][knob] = start_value
            for i in range(start_frame+1, end_frame):
                knoblist[i][knob] = start_value + value_delta * i

    for i in range(frames):
        knobs = knoblist[i]
        for knob in knobs.keys():
            symbols[knob] = ['knob', knobs[knob]]
        clear_screen( screen )
        clear_zbuffer( zbuffer )
        tmp = new_matrix()
        ident( tmp )

        stack = [ [x[:] for x in tmp] ]
        for command in commands:
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
                if command['constants']:
                    reflect = command['constants']
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
            elif c == 'move':
                knob = command['knob']
                val = symbols[knob][1] if knob else 1
                tmp = make_translate(args[0]*val, args[1]*val, args[2]*val)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                knob = command['knob']
                val = symbols[knob][1] if knob else 1
                tmp = make_scale(val*args[0], val*args[1], val*args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                knob = command['knob']
                val = symbols[knob][1] if knob else 1
                theta = args[1] * (math.pi/180) * val
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
            # elif c == 'display':
            #     display(screen)
            # elif c == 'save':
            #     save_extension(screen, args[0])
        save_extension(screen, basename + ('%d.png' % i))
