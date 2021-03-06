import matplotlib.pyplot as plt

def plot_it(x,degree,n):
    f = open(x)
    lines = f.readlines()
    f.close()

    line = lines[n-1]
    data = [float(x) for x in line.split()]
    
    y = data[2:]
    new_y = []
    for x in range(degree-1,len(y)):
        q = sum([y[x-z] for z in range(degree)])/degree
        new_y.append(q)

    t = [x*data[1] for x in range(0,len(new_y))]

    plt.plot(t,new_y,linewidth=1)
    plt.grid(True)
    plt.savefig('simple_draw1/pic'+str(n)+'.svg')
    plt.clf()

for x in range(1,33):    
    plot_it('out1.dat',150,x)
