from subprocess import Popen, PIPE
# big thanks to lantao &
# CAS Key Laboratory of Basic Plasma Physics ~
f = open('out1.dat', 'w')
for x in range(1, 33):

    process = Popen(['octave','./lsfreader.m', 'raw_data1/ALL' +
                    str(x).zfill(4)+'/A0000CH1.LSF'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    s = str(stdout.decode()).split('\n')
    o = []
    for w in s:
        last_non_zero = 0
        for y in range(len(w)):
            if w[y] != '0':
                last_non_zero = y
        o.append(w[:last_non_zero+1])
    f.write(str(x)+' '+''.join(o)+'\n')
f.close()
