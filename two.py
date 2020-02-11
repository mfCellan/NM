import math as m

def p(x):
    return 1


def q(x):
    return -x


def f(x):
    return 2 + 2 * x - x * x * x


def y_sol(x):
    return x * x


def dy_sol(x):
    return 2 * x


def ddy_sol(x):
    return 2


def Discrepancy(x, y, n):
    dscr = 0
    t1 = 0
    t2 = 0
    for i in range(1, n + 1):
        t1 = abs(y[i] - y_sol(a0 + i * h))
        if t1 > t2:
            dscr = t1
        else:
            dscr = t2

    return dscr


def DscrOfTMA(x, y, n):
    dscr = 0
    for i in range(1, n):
        t = a[i] * y[i - 1] + b[i] * y[i] + c[i] * y[i + 1] - d[i]
        dscr += t * t

    return m.sqrt(dscr)


def TMA(a, b, c, f, y, n):
    alpha = [0] * (n + 1)
    beta = [0] * (n + 1)

    alpha[2] = -c[1] / b[1]
    beta[2] = d[1] / b[1]
    for i in range(2, n):
        zn = a[i] * alpha[i] + b[i]
        alpha[i + 1] = -c[i] / zn
        beta[i + 1] = (d[i] - a[i] * beta[i]) / zn
    y[n] = (d[n] - a[n] * beta[n]) / (b[n] + a[n] * alpha[n])
    for i in range(n - 1, 0, -1):
        y[i] = alpha[i + 1] * y[i + 1] + beta[i + 1]
    y[0] = alpha[1] * y[1] + beta[1]


##################################################################

a0 = 0
b0 = 1
n = 10

##################
a = [0] * (n + 1)
b = [0] * (n + 1)
c = [0] * (n + 1)
d = [0] * (n + 1)
y = [0] * (n + 1)
x = [0] * (n + 1)
##################

h = (b0 - a0) / n
h_2 = h / 2
h2 = h ** 2

for k in range(n + 1):
    x_k = a0 + k * h
    a[k] = 1 - h_2 * p(x_k)
    b[k] = h2 * q(x_k) - 2
    c[k] = 1 + h_2 * p(x_k)
    d[k] = h2 * f(x_k)

a[0] = 0
b[0] = 1
c[0] = -1
d[0] = -h * dy_sol(a0)

a[n] = -1.
b[n] = 1.
c[n] = 0
d[n] = h * dy_sol(b0)

TMA(a, b, c, d, y, n)

for k in range(n + 1):
    print('y(', k, ') calc:', y[k])
    print('        acc:', y_sol(a0 + k * h))
    print()

print()
print('h =', h)
print('Discrepancy of TMA:', DscrOfTMA(x, y, n))
print('Discrepancy:', Discrepancy(x, y, n))
