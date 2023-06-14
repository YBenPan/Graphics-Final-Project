from display import *
from matrix import *
from gmath import *
import json

def draw_scanline(x0, z0, x1, z1, y, nx0, ny0, nz0, nx1, ny1, nz1, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample):
    if x0 > x1:
        # tx = x0
        # tz = z0
        # x0 = x1
        # z0 = z1
        # x1 = tx
        # z1 = tz
        x0, x1 = x1, x0
        z0, z1 = z1, z0
        nx0, nx1 = nx1, nx0
        ny0, ny1 = ny1, ny0
        nz0, nz1 = nz1, nz0

    dist_x = x1 - x0 + 1
    x = x0
    z = z0
    delta_z = (z1 - z0) / dist_x if dist_x != 0 else 0

    nx = nx0
    ny = ny0
    nz = nz0
    delta_nx = (nx1 - nx0) / dist_x if dist_x != 0 else 0
    delta_ny = (ny1 - ny0) / dist_x if dist_x != 0 else 0
    delta_nz = (nz1 - nz0) / dist_x if dist_x != 0 else 0

    while x <= x1:
        normal = [nx, ny, nz]
        # Backface culling?
        # if dot_product(normal, view) > 0:
        if 1:
            color = get_lighting(normal, view, ambient, lights, symbols, reflect )
            plot(screen, zbuffer, color, x, y, z, supersample)
        x += 1
        z += delta_z
        nx += delta_nx
        ny += delta_ny
        nz += delta_nz

def scanline_convert(polygons, normalMap, i, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]


    points.sort(key = lambda x: x[1])
    vertexNorms = []
    vertexNorms.append(vector_avg(normalMap[points[BOT]]))
    vertexNorms.append(vector_avg(normalMap[points[MID]]))
    vertexNorms.append(vector_avg(normalMap[points[TOP]]))

    yb = int(points[0][1])
    ym = int(points[1][1])
    yt = int(points[2][1])

    xb = int(points[0][0])
    xm = int(points[1][0])
    xt = int(points[2][0])

    zb = int(points[0][2])
    zm = int(points[1][2])
    zt = int(points[2][2])

    # print("Y Values")
    # print(yb, ym, yt)

    # print("Normals")
    # print(vertexNorms)
    # input()

    for i in range(supersample):
        for j in range(supersample):
            x0 = xb * supersample + i
            x1 = xb * supersample + i

            z0 = zb
            z1 = zb

            y = yb * supersample + j

            nx0, ny0, nz0 = vertexNorms[BOT]
            nx1, ny1, nz1 = vertexNorms[BOT]

            distance0 = yt * supersample + j - y + 1
            distance1 = ym * supersample + j - y
            distance2 = yt * supersample - ym * supersample + 1

            # print("Distances:")
            # print(distance0, distance1, distance2)

            dnx0 = (vertexNorms[TOP][0] - vertexNorms[BOT][0]) / distance0 if distance0 != 0 else 0
            dny0 = (vertexNorms[TOP][1] - vertexNorms[BOT][1]) / distance0 if distance0 != 0 else 0
            dnz0 = (vertexNorms[TOP][2] - vertexNorms[BOT][2]) / distance0 if distance0 != 0 else 0
            dnx1 = (vertexNorms[MID][0] - vertexNorms[BOT][0]) / distance1 if distance1 != 0 else 0
            dny1 = (vertexNorms[MID][1] - vertexNorms[BOT][1]) / distance1 if distance1 != 0 else 0
            dnz1 = (vertexNorms[MID][2] - vertexNorms[BOT][2]) / distance1 if distance1 != 0 else 0

            # print("D Values:")
            # print(dnx0, dny0, dnz0, dnx1, dny1, dnz1)


            while y < ym * supersample + j:
                # print(x0, x1, y)
                # print(500-1-int(y/supersample), int(x0/supersample))
                # input()
                if 500-1-int(y/supersample) >= 0 and 500-1-int(y/supersample) < 500:
                    if int(x0/supersample) > 0 and int(x0/supersample) < 500:
                        reduced_screen[500-1-int(y/supersample)][int(x0/supersample)] = 1
                    if int(x1/supersample) > 0 and int(x1/supersample) < 500:
                        reduced_screen[500-1-int(y/supersample)][int(x1/supersample)] = 1
                normal = [nx0, ny0, nz0]
                normalize(normal)
                color = get_lighting(normal, view, ambient, lights, symbols, reflect )
                plot(screen, zbuffer, color, int(x0), int(y), z0, supersample)
                normal = [nx1, ny1, nz1]
                normalize(normal)
                color = get_lighting(normal, view, ambient, lights, symbols, reflect )
                plot(screen, zbuffer, color, int(x1), int(y), z1, supersample)
                if i == 0 and j == 0 or y == ym * supersample + j - 1:
                    if x0 < x1:
                        draw_scanline(int(x0)+1, z0, int(x1)-1, z1, int(y), nx0, ny0, nz0, nx1, ny1, nz1, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample)
                    else:
                        draw_scanline(int(x0)-1, z0, int(x1)+1, z1, int(y), nx0, ny0, nz0, nx1, ny1, nz1, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample)
                if (xt != xb):
                    x0 += (xt-xb)/(yt-yb+1)
                if (xm != xb):
                    x1 += (xm-xb)/(ym-yb)
                if (zt != zb):
                    z0 += (zt-zb)/(yt-yb+1)
                if (zm != zb):
                    z1 += (zm-zb)/(ym-yb)
                y += 1
                nx0 += dnx0
                ny0 += dny0
                nz0 += dnz0
                nx1 += dnx1
                ny1 += dny1
                nz1 += dnz1
            # print("MID:")
            # print(nx0, ny0, nz0, nx1, ny1, nz1)
            # input()
            x1 = xm * supersample + i
            z1 = zm
            nx1 = vertexNorms[MID][0]
            ny1 = vertexNorms[MID][1]
            nz1 = vertexNorms[MID][2]
            dnx1 = (vertexNorms[TOP][0] - vertexNorms[MID][0]) / distance2 if distance2 != 0 else 0
            dny1 = (vertexNorms[TOP][1] - vertexNorms[MID][1]) / distance2 if distance2 != 0 else 0
            dnz1 = (vertexNorms[TOP][2] - vertexNorms[MID][2]) / distance2 if distance2 != 0 else 0
            # print("MID POST SWITCH:")
            # print(nx0, ny0, nz0, nx1, ny1, nz1)
            # input()

            while y <= yt * supersample + j:
                if 500-1-int(y/supersample) >= 0 and 500-1-int(y/supersample) < 500:
                    if int(x0/supersample) >= 0 and int(x0/supersample) < 500:
                        reduced_screen[500-1-int(y/supersample)][int(x0/supersample)] = 1
                    if int(x1/supersample) >= 0 and int(x1/supersample) < 500:
                        reduced_screen[500-1-int(y/supersample)][int(x1/supersample)] = 1
                normal = [nx0, ny0, nz0]
                normalize(normal)
                color = get_lighting(normal, view, ambient, lights, symbols, reflect )
                plot(screen, zbuffer, color, int(x0), int(y), z0, supersample)
                normal = [nx1, ny1, nz1]
                normalize(normal)
                color = get_lighting(normal, view, ambient, lights, symbols, reflect )
                plot(screen, zbuffer, color, int(x1), int(y), z1, supersample)
                if i == 0 and j == 0 or y == ym * supersample + j - 1:
                    if x0 < x1:
                        draw_scanline(int(x0)+1, z0, int(x1)-1, z1, int(y), nx0, ny0, nz0, nx1, ny1, nz1, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample)
                    else:
                        draw_scanline(int(x0)-1, z0, int(x1)+1, z1, int(y), nx0, ny0, nz0, nx1, ny1, nz1, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample)
                if (xt != xb):
                    x0 += (xt-xb)/(yt-yb+1)
                if (xt != xm):
                    x1 += (xt-xm)/(yt-ym+1)
                if (zt != zb):
                    z0 += (zt-zb)/(yt-yb+1)
                if (zt != zm):
                    z1 += (zt-zm)/(yt-ym+1)
                y += 1
                nx0 += dnx0
                ny0 += dny0
                nz0 += dnz0
                nx1 += dnx1
                ny1 += dny1
                nz1 += dnz1
            draw_scanline(int(x0), z0, int(x1), z1, int(y), nx0, ny0, nz0, nx1, ny1, nz1, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample)
            # print("FINAL:")
            # print(nx0, ny0, nz0, nx1, ny1, nz1)
            # input()


def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)


def add_mesh( polygons, vertexList, faceList):
    for i, face in enumerate(faceList):
        x0, y0, z0 = vertexList[face[0]]
        x1, y1, z1 = vertexList[face[1]]
        x2, y2, z2 = vertexList[face[2]]
        add_polygon(polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2)
        # if i % 1000 == 0:
        #     print(i)

def draw_polygons( polygons, normalMap, screen, zbuffer, reduced_screen, view, ambient, lights, symbols, reflect, supersample):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return
    t = view[0][:3]
    view = t[:]
    view = [-x for x in view]
    # print(view)

    point = 0
    while point < len(polygons) - 2:
        normal = calculate_normal(polygons, point)[:]
        x0, y0, z0 = polygons[point][:3]
        x1, y1, z1 = polygons[point + 1][:3]
        x2, y2, z2 = polygons[point + 2][:3]
        normalMap[(x0, y0, z0)] = normalMap.get((x0, y0, z0), []) + [normal]
        normalMap[(x1, y1, z1)] = normalMap.get((x1, y1, z1), []) + [normal]
        normalMap[(x2, y2, z2)] = normalMap.get((x2, y2, z2), []) + [normal]
        point += 3

    point = 0
    while point < len(polygons) - 2:
        normal = calculate_normal(polygons, point)[:]
        if dot_product(normal, view) > 0:
            scanline_convert(polygons, normalMap, point, view, ambient, lights, symbols, reflect, screen, zbuffer, reduced_screen, supersample)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons,
                             points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons,
                             points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            if (longt == (step - 1)):
                p1 = p0 - longt
            else:
                p1 = p0 + 1
            p2 = (p1 + step) % (step * step)
            p3 = (p0 + step) % (step * step)

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx
            y = r0 * math.sin(2*math.pi * circ) + cy
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx
        y1 = r * math.sin(2*math.pi * t) + cy

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, reduced_screen, color, supersample ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, reduced_screen, color, supersample)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )

def reduce( screen, reduced_screen, supersample ):
    ns = new_screen()
    zbuf = new_zbuffer()
    for i in range(int(len(screen)/supersample)):
        for j in range(int(len(screen)/supersample)):
            if reduced_screen[i][j]:
                val = [0, 0, 0]
                for x in range(supersample):
                    for y in range(supersample):
                        #print(val)
                        val = [val[k] + screen[i*supersample+x][j*supersample+y][k] for k in range(3)]
                val = [int(val[i] / (supersample**2)) for i in range(3)]
                if val != [0, 0, 0]:
                    plot(ns, zbuf, val, j, 500-1-i, 0)
            else:
                plot(ns, zbuf, screen[i*supersample][j*supersample], j, 500-1-i, 0)
    return ns

def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, reduced_screen, color, supersample=1 ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x0orig = x0
    x1orig = x1
    y0orig = y0
    y1orig = y1
    for i in range(supersample):
        for j in range(supersample):
            x0 = x0orig*supersample+i
            x1 = x1orig*supersample+i
            y0 = y0orig*supersample+j
            y1 = y1orig*supersample+j
            x = x0
            y = y0
            z = z0
            A = 2 * (y1 - y0)
            B = -2 * (x1 - x0)
            wide = False
            tall = False

            if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
                wide = True
                loop_start = x
                loop_end = x1
                dx_east = dx_northeast = 1
                dy_east = 0
                d_east = A
                distance = x1 - x + 1
                if ( A > 0 ): #octant 1
                    d = A + B/2
                    dy_northeast = 1
                    d_northeast = A + B
                else: #octant 8
                    d = A - B/2
                    dy_northeast = -1
                    d_northeast = A - B

            else: #octants 2/7
                tall = True
                dx_east = 0
                dx_northeast = 1
                distance = abs(y1 - y) + 1
                if ( A > 0 ): #octant 2
                    d = A/2 + B
                    dy_east = dy_northeast = 1
                    d_northeast = A + B
                    d_east = B
                    loop_start = y
                    loop_end = y1
                else: #octant 7
                    d = A/2 - B
                    dy_east = dy_northeast = -1
                    d_northeast = A - B
                    d_east = -1 * B
                    loop_start = y1
                    loop_end = y

            dz = (z1 - z0) / distance if distance != 0 else 0

            while ( loop_start < loop_end ):
                reduced_screen[500-1-int(y/supersample)][int(x/supersample)] = 1
                plot( screen, zbuffer, color, x, y, z, supersample)
                if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
                     (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

                    x+= dx_northeast
                    y+= dy_northeast
                    d+= d_northeast
                else:
                    x+= dx_east
                    y+= dy_east
                    d+= d_east
                z+= dz
                loop_start+= 1
            reduced_screen[500-1-int(y/supersample)][int(x/supersample)] = 1
            plot( screen, zbuffer, color, x, y, z, supersample)
