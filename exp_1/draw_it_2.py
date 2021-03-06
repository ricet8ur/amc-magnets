import matplotlib.pyplot as plt

def plot_it(x,n):
    f = open(x)
    lines = f.readlines()
    f.close()

    line = lines[n-1]
    data = [float(x) for x in line.split()]
    
    y = data[2:]
    x = [x*data[1] for x in range(0,len(y))]

    plt.plot(x,y,linewidth=0.1)
    plt.savefig('raw_draw1/pic'+str(n)+'.svg')
    plt.clf()

for x in range(1,33):    
    plot_it('out1.dat',x)
