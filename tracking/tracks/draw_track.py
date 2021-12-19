import matplotlib.pyplot as plt
import numpy as np

sz = 0.21

def plot_it(x,n):
    f = open(x+str(n)+'.txt')
    lines = f.readlines()
    f.close()

    data = [tuple(float(y) for y in x.split()) for x in lines]
    
    y = [p[2] for p in data]
    x = [p[1] for p in data]
    # box points
    
    a = [(p[3], p[4]) for p in data]
    b = [(p[5], p[6]) for p in data]
    # g = [(b[p][0]-a[p][0],b[p][1]-a[p][1]) for p in range(len(a))]
    # n = [(n[p][0)) for p in range(len(n))]

    q = sz/(sum([abs(a[p][0]-b[p][0]) for p in range(len(a))])/len(a))

    for p in range(len(a)):
        x[p] -= a[p][0]
        y[p] -= a[p][1]

    idx = [p for p in range(len(x)) if q*x[p]>0.0 and q*x[p]<10.0]
    plt.scatter([q*x[p] for p in idx],[-q*y[p] for p in idx])
    # plt.axis('square')
    plt.xlabel('x, м')
    plt.ylabel('y, м')
    plt.grid(True)
    plt.yticks(np.arange(0, 0.25, 0.05))
    plt.xticks(np.arange(-0.05, 0.25, 0.05))


for x in range(4,5):    
    plot_it('u2/',x)
plt.savefig('pic/result3'+'.svg')
plt.clf()