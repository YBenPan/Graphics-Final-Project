import mdl
import os
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

    # Create animation folder
    os.makedirs("gif", exist_ok=True)

    color = [255, 255, 255]
    tmp = new_matrix()
    ident(tmp)
    ident( tmp )
    normalMap = {}

    stack = [ [x[:] for x in tmp] ]
    supersample = 1
    screen = new_screen(500*supersample, 500*supersample)
    zbuffer = new_zbuffer(500*supersample, 500*supersample)
    reduced_screen = [[0 for x in range(500)] for y in range(500)]
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

    # Check for animation keywords
    frames = False
    basename = False
    vary = False

    print("All symbols:")
    print(symbols)
    print()
    print("Press any key to continue...")
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
        if frames > 1:
            knobs = knoblist[i]
            for knob in knobs.keys():
                symbols[knob] = ['knob', knobs[knob]]
        clear_screen( screen )
        clear_zbuffer( zbuffer )
        reduced_screen = [[0 for x in range(500)] for y in range(500)]
        tmp = []

        # Set camera
        view = [[0, 0, -1, 1]]
        viewing_transform = new_matrix() # Separate from all other transformation matrices
        ident(viewing_transform)
        stack = [[x[:] for x in viewing_transform]]
        if 'camera' in symbols:
            # TODO: Fix rotate camera. Rotate camera first then translate
            if 'eye' in symbols['camera'][1]:
                # Translate camera by taking the inverse of transformation in the model scene
                eye_x, eye_y, eye_z = symbols['camera'][1]['eye']
                camera_trans = make_translate(-eye_x, -eye_y, -eye_z)
                matrix_mult(camera_trans, viewing_transform)
            # if 'aim' in symbols['camera'][1]:
            #     view = symbols['camera'][1]['aim']
            #     normalize(view)

        for command in commands:
            c = command['op']
            args = command['args']
            print(f"Processing: {c}")

            if c == 'box':
                if command['constants']:
                    reflect = command['constants']
                add_box(tmp,
                        args[0], args[1], args[2],
                        args[3], args[4], args[5])
                matrix_mult( viewing_transform, tmp)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, normalMap, screen, zbuffer, reduced_screen, view, ambient, lights, symbols, reflect, supersample)
                tmp = []
                normalMap = {}
                reflect = '.white'
            elif c == 'sphere':
                if command['constants']:
                    reflect = command['constants']
                add_sphere(tmp,
                           args[0], args[1], args[2], args[3], step_3d)
                matrix_mult( viewing_transform, tmp)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, normalMap, screen, zbuffer, reduced_screen, view, ambient, lights, symbols, reflect, supersample)
                tmp = []
                normalMap = {}
                reflect = '.white'
            elif c == 'torus':
                if command['constants']:
                    reflect = command['constants']
                add_torus(tmp,
                          args[0], args[1], args[2], args[3], args[4], step_3d)
                matrix_mult( viewing_transform, tmp)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, normalMap, screen, zbuffer, reduced_screen, view, ambient, lights, symbols, reflect, supersample)
                tmp = []
                normalMap = {}
                reflect = '.white'
            elif c == 'mesh':
                if command['constants']:
                    reflect = command['constants']
                filename = f"{command['args'][0]}.obj"
                vertexList = []
                faceList = []
                with open(filename) as file:
                    for i, line in enumerate(file):
                        line = line.rstrip()
                        if len(line) >= 6 and line[:6] == 'mtllib':
                            # Import associated MTL file
                            mtl_filename = line[7:]
                            with open(mtl_filename) as mtl_file:
                                m_name = ''
                                for j, m_line in enumerate(mtl_file):
                                    m_line = m_line.strip()
                                    if len(m_line) >= 6 and m_line[:6] == 'newmtl':
                                        m_name = m_line[7:]
                                        symbols[m_name] = ['constants', 
                                                           {'red' : [0.2, 0.5, 0.5], 
                                                            'green' : [0.2, 0.5, 0.5], 
                                                            'blue' : [0.2, 0.5, 0.5],
                                                            'spec_coeff': SPECULAR_EXP}]
                                    elif len(m_line) >= 4 and m_line[:2] == 'Ka':
                                        coeffs = m_line[3:].split()
                                        symbols[m_name][1]['red'][0] = float(coeffs[0])
                                        symbols[m_name][1]['green'][0] = float(coeffs[1])
                                        symbols[m_name][1]['blue'][0] = float(coeffs[2])
                                    elif len(m_line) >= 4 and m_line[:2] == 'Kd':
                                        coeffs = m_line[3:].split()
                                        symbols[m_name][1]['red'][1] = float(coeffs[0])
                                        symbols[m_name][1]['green'][1] = float(coeffs[1])
                                        symbols[m_name][1]['blue'][1] = float(coeffs[2])
                                    elif len(m_line) >= 4 and m_line[:2] == 'Ks':
                                        coeffs = m_line[3:].split()
                                        symbols[m_name][1]['red'][2] = float(coeffs[0])
                                        symbols[m_name][1]['green'][2] = float(coeffs[1])
                                        symbols[m_name][1]['blue'][2] = float(coeffs[2])
                                    elif len(m_line) >= 4 and m_line[:2] == 'Ns':  
                                        symbols[m_name][1]['spec_exp'] = float(m_line[3:])                
                        elif line[:2] == 'v ':
                            vertexList.append([float(coord) for coord in line[2:].split()])
                print("Symbol table after importing the MTL file:")
                print(symbols)
                print()
                print("Press any key to continue...")
                input()
                with open(filename) as file:
                    for i, line in enumerate(file):
                        line = line.rstrip()
                        if len(line) >= 6 and line[:6] == 'usemtl':
                            if len(faceList) > 0:
                                print(f"Done: {reflect}")
                                add_mesh(tmp, vertexList, faceList)
                                matrix_mult( viewing_transform, tmp)
                                matrix_mult( stack[-1], tmp )
                                draw_polygons(tmp, normalMap, screen, zbuffer, reduced_screen, view, ambient, lights, symbols, reflect, supersample)
                                faceList = []
                            mtl_name = line[7:]
                            reflect = mtl_name
                        elif line[:2] == 'f ':
                            vertices = line[2:].split()
                            v_indices = [int(str.split('/')[0]) for str in vertices]
                            for j in range(1, len(v_indices) - 1):
                                faceList.append([v_indices[0] - 1, v_indices[j] - 1, v_indices[j + 1] - 1])                            
                add_mesh(tmp, vertexList, faceList)
                matrix_mult( viewing_transform, tmp)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, normalMap, screen, zbuffer, reduced_screen, view, ambient, lights, symbols, reflect, supersample)
                tmp = []
                normalMap = {}
                reflect = '.white'
            elif c == 'line':
                add_edge(tmp,
                         args[0], args[1], args[2], args[3], args[4], args[5])
                matrix_mult( viewing_transform, tmp)
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
            elif c == 'move':
                knob = command['knob'] if command['knob'] else None
                val = symbols[knob][1] if knob else 1
                tmp = make_translate(args[0]*val, args[1]*val, args[2]*val)
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'scale':
                knob = command['knob'] if command['knob'] else None
                val = symbols[knob][1] if knob else 1
                tmp = make_scale(val*args[0], val*args[1], val*args[2])
                matrix_mult(stack[-1], tmp)
                stack[-1] = [x[:] for x in tmp]
                tmp = []
            elif c == 'rotate':
                knob = command['knob'] if command['knob'] else None
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
            elif c == 'rotcam':
                theta = args[1] * (math.pi/180)
                if args[0] == 'x':
                    tmp = make_rotX(-theta)
                elif args[0] == 'y':
                    tmp = make_rotY(-theta)
                else:
                    tmp = make_rotZ(-theta)
                tmp_view = [x[:] for x in tmp]
                matrix_mult(tmp_view, view)
                matrix_mult(viewing_transform, tmp)
                viewing_transform = [x[:] for x in tmp]
                # print("Viewing Transform:", viewing_transform)
                # input()
                tmp = []
            elif c == 'push':
                stack.append([x[:] for x in stack[-1]] )
            elif c == 'pop':
                stack.pop()
            if frames == 1:
                if c == 'display':
                    display(screen)
                    if supersample > 1:
                        screen = reduce(screen, reduced_screen, supersample)
                        display(screen)
                elif c == 'save':
                    save_extension(screen, args[0])
        if frames > 1:
            save_extension(screen, 'gif/' + basename + ('%d.png' % i).zfill(8))
        else:
            save_extension(screen, 'image.png')
    if frames > 1:
        convert_to_gif(basename, 'animated.gif')
        show_gif('animated.gif')
