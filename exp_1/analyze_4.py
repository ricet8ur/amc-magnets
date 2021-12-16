import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq
from scipy import signal


def plot_it(x, degree, n):
    f = open(x)
    lines = f.readlines()
    f.close()

    line = lines[n-1]
    data = [float(x) for x in line.split()]
    y = data[2:]
    new_y = []
    for x in range(degree-1, len(y)):
        q = sum([y[x-z] for z in range(degree)])/degree
        new_y.append(q)
    t = [x*data[1] for x in range(0, len(new_y))]

    y = np.array(new_y)
    y = y - y.mean()

    peaks = []
    for p in range(1, 5):
        f_signal = fft(np.concatenate((np.array([0 for x in range(10000)]),
         y[(p-1)*y.size//4:(p)*y.size//4]), axis=None))
        w = fftfreq(f_signal.size, d=(t[1]-t[0]))
        # print(w[:5])
        m_freq = w[signal.find_peaks_cwt(
            abs(f_signal)**2, np.arange(1, 100))[0]]
        peaks.append(m_freq)
        # print(w[:10])
        plt.subplot(2, 4, p)
        plt.xlabel('Frequency (Hz)\n max freq: '+str(round(m_freq, 2)))
        plt.plot(w, abs(f_signal)**2)
        plt.xticks(np.arange(0, 80, 20))
# plt.yticks(np.arange(0, 11, 1))
        plt.xlim(0, 80)
        plt.grid(True)

    plt.subplot(5, 1, 4)
    plt.plot(t, new_y)
    plt.xlabel('time\nmax freq: '+str(round(max(peaks), 2)))
    plt.xticks(np.arange(0, 0.5, 0.05))
    plt.grid(True)
    plt.savefig('results1/pic'+str(n)+'.svg', dpi=300)
    plt.clf()


for x in range(1, 33):
    plot_it('out1.dat', 150, x)
