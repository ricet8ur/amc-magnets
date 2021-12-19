import math

mu_0 = 4 * math.pi * 10 ** (-7)


def modelling(pho, l, mass, r, v0, t, M=900000, dt=0.01):
    # pho - прицельный параметр, l - расстояние от горки до горки, mass - масса шарика, r - радиус шарика, M - намагниченность, dt - время между итерациями.
    # Указывать все величины в СИ!!!
    x_t = {}
    y_t = {}
    curT, curX, curY = 0.00, l / 2, pho / 2
    curVx, curVy = -v0, 0
    m = 4 / 3 * math.pi * M * r**3
    c = 3 * mu_0 * m * m / 32 / math.pi / mass

    x_t[curT], y_t[curT] = curX, curY

    while curT < t:
        curT += dt
        curX, curY, curVx, curVy = iteration(curX, curY, curVx, curVy, c, dt)
        x_t[curT], y_t[curT] = curX, curY
        if curX**2+curY**2 < r**2:
            break
    return x_t, y_t


def iteration(curX, curY, curVx, curVy, c, dt):
    aX, aY = -c * curX * (curX ** 2 + curY ** 2) ** (-2.5), -c * curY * (curX ** 2 + curY ** 2) ** (-2.5)
    newX, newY, newVx, newVy = curX + curVx * dt, curY + curVy * dt, curVx + aX * dt, curVy + aY * dt
    return newX, newY, newVx, newVy


def output(x_t, y_t, r, dt, t):
    # На первой строке файле указывается время между итерациями, числа разделены точкой с запятой ';'
    with open('data2.csv', 'w+') as f:
        f.write(str(dt) + ' '+str(r)+'\n')
        curT = 0.00
        while curT < t:
            curT += dt
            if curT not in x_t:
                break
            xx, yy = x_t[curT], y_t[curT]
            f.write(str(xx) + ";" + str(yy))
            if curT + dt < t:
              f.write("\n")

output(*modelling( 0.023,  0.208, 0.003855,0.005,0.5,3,dt=0.001), 0.005,0.001, 3)